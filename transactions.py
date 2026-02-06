from blockchain import Blockchain
from rbac import SeafoodRBAC
from datetime import datetime

# =========================
# CONFIG-DRIVEN WORKFLOW
# =========================

WORKFLOW_RULES = {
    "CREATE_BATCH": {
        "allowed_roles": ["Fisherman"],
        "previous_event": None
    },
    "TRANSFER": {
        "allowed_roles": ["Distributor"],
        "previous_event": "CREATE_BATCH"
    },
    "TRANSPORT_UPDATE": {
        "allowed_roles": ["Transporter"],
        "previous_event": "TRANSFER"
    },
    "RETAIL_RECEIPT": {
        "allowed_roles": ["Retailer"],
        "previous_event": "TRANSPORT_UPDATE"
    }
}

CERTIFIED_FISHERMEN = {"F001"}  # demo certification authority


class SeafoodTransactions:
    def __init__(self):
        self.blockchain = Blockchain()
        self.rbac = SeafoodRBAC()
        self.batches = {}
        self.last_event = {}
        self._rebuild_state_from_chain()

    # =========================
    # REBUILD STATE FROM CHAIN
    # =========================
    def _rebuild_state_from_chain(self):
        for block in self.blockchain.chain:
            data = block.data
            event = data.get("event")
            batch_id = data.get("batch_id")

            if not batch_id:
                continue

            if event == "CREATE_BATCH":
                self.batches[batch_id] = {
                    "species": data["species"],
                    "weight": data["weight"],
                    "owner": data["owner"],
                    "location": data["location"],
                    "certified": data.get("certified", False)
                }
                self.last_event[batch_id] = "CREATE_BATCH"
                continue

            if batch_id not in self.batches:
                continue

            self.batches[batch_id]["owner"] = data.get(
                "owner", self.batches[batch_id]["owner"]
            )

            self.batches[batch_id]["location"] = data.get(
                "location", self.batches[batch_id]["location"]
            )

            self.last_event[batch_id] = event

    # =========================
    # VALIDATORS
    # =========================
    def _validate_hierarchy(self, batch_id, new_event):
        rule = WORKFLOW_RULES[new_event]
        expected_prev = rule["previous_event"]
        actual_prev = self.last_event.get(batch_id)

        if expected_prev != actual_prev:
            return False, f"Invalid order: expected {expected_prev}, got {actual_prev}"
        return True, None

    def _validate_species_weight(self, batch_id, species, weight):
        batch = self.batches.get(batch_id)
        if not batch:
            return False, "Batch does not exist"

        if batch["species"] != species:
            return False, "Species mismatch"

        if float(batch["weight"]) != float(weight):
            return False, "Weight mismatch"

        return True, None

    # =========================
    # CREATE BATCH (GENESIS)
    # =========================
    def create_batch(self, pid, batch_id, species, weight, location, certified_claim):
        if not self.rbac.can_perform_action(pid, "create_batch"):
            return {"success": False, "message": "Only Fisherman can create batches"}

        if batch_id in self.batches:
            return {"success": False, "message": "Duplicate batch ID"}

        certified = certified_claim and pid in CERTIFIED_FISHERMEN

        block = {
            "event": "CREATE_BATCH",
            "batch_id": batch_id,
            "species": species,
            "weight": weight,
            "from": "OCEAN",
            "to": pid,
            "owner": pid,
            "location": location,
            "certified": certified,
            "details": f"Batch caught from ocean at {location}",
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M:%S")
        }

        self.blockchain.add_block(block)

        self.batches[batch_id] = {
            "species": species,
            "weight": weight,
            "owner": pid,
            "location": location,
            "certified": certified
        }
        self.last_event[batch_id] = "CREATE_BATCH"

        return {"success": True, "message": "Batch created from ocean"}

    # =========================
    # TRANSFER OWNERSHIP
    # =========================
    def transfer_ownership(self, pid, batch_id, new_owner, species, weight, location):
        if not self.rbac.can_perform_action(pid, "transfer_batch"):
            return {"success": False, "message": "Only Distributor can transfer ownership"}

        ok, err = self._validate_hierarchy(batch_id, "TRANSFER")
        if not ok:
            return {"success": False, "message": err}

        ok, err = self._validate_species_weight(batch_id, species, weight)
        if not ok:
            return {"success": False, "message": err}

        old_owner = self.batches[batch_id]["owner"]

        block = {
            "event": "TRANSFER",
            "batch_id": batch_id,
            "species": species,
            "weight": weight,
            "from": old_owner,
            "to": new_owner,
            "owner": new_owner,
            "location": location,
            "certified": self.batches[batch_id]["certified"],
            "details": f"Ownership transferred from {old_owner} to {new_owner} at {location}",
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M:%S")
        }

        self.blockchain.add_block(block)

        self.batches[batch_id]["owner"] = new_owner
        self.batches[batch_id]["location"] = location
        self.last_event[batch_id] = "TRANSFER"

        return {"success": True, "message": "Ownership transferred"}

    # =========================
    # TRANSPORT UPDATE
    # =========================
    def update_transport(self, pid, batch_id, species, weight, location, details):
        if not self.rbac.can_perform_action(pid, "update_transport"):
            return {"success": False, "message": "Only Transporter can update transport"}

        ok, err = self._validate_hierarchy(batch_id, "TRANSPORT_UPDATE")
        if not ok:
            return {"success": False, "message": err}

        ok, err = self._validate_species_weight(batch_id, species, weight)
        if not ok:
            return {"success": False, "message": err}

        details = f"Batch transported to {location} using temperature-controlled logistics"

        owner = self.batches[batch_id]["owner"]

        block = {
            "event": "TRANSPORT_UPDATE",
            "batch_id": batch_id,
            "species": species,
            "weight": weight,
            "from": owner,
            "to": owner,
            "owner": owner,
            "location": location,
            "details": details,
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M:%S")
        }

        self.blockchain.add_block(block)

        self.batches[batch_id]["location"] = location
        self.last_event[batch_id] = "TRANSPORT_UPDATE"

        return {"success": True, "message": "Transport updated"}
    
    # =========================
    # RETAIL RECEIPT (FINAL)
    # =========================
    def retail_receipt(self, pid, batch_id, species, weight, location):
        if not self.rbac.can_perform_action(pid, "receive_delivery"):
            return {"success": False, "message": "Only Retailer can confirm receipt"}

        ok, err = self._validate_hierarchy(batch_id, "RETAIL_RECEIPT")
        if not ok:
            return {"success": False, "message": err}

        ok, err = self._validate_species_weight(batch_id, species, weight)
        if not ok:
            return {"success": False, "message": err}

        previous_owner = self.batches[batch_id]["owner"]

        block = {
            "event": "RETAIL_RECEIPT",
            "batch_id": batch_id,
            "species": species,
            "weight": weight,
            "from": previous_owner,
            "to": pid,
            "owner": pid,
            "location": location,
            "certified": self.batches[batch_id]["certified"],
            "details": f"Batch received by retailer at {location} and ready for consumer sale",
            "timestamp": datetime.now().strftime("%d %b %Y, %H:%M:%S")
        }

        self.blockchain.add_block(block)

        self.batches[batch_id]["owner"] = pid
        self.batches[batch_id]["location"] = location
        self.last_event[batch_id] = "RETAIL_RECEIPT"

        return {"success": True, "message": "Retail receipt confirmed"}


    # =========================
    # HISTORY (QR / UI)
    # =========================
    def get_batch_history(self, batch_id):
        return [
            block.data
            for block in self.blockchain.chain
            if block.data.get("batch_id") == batch_id
        ]
    
    