from blockchain import Blockchain
from rbac import SeafoodRBAC
from datetime import datetime


class SeafoodTransactions:
    """
    Simulated smart contract enforcing:
    - strict workflow
    - immutable weight & species
    - uniform blockchain event structure
    """

    def __init__(self):
        self.blockchain = Blockchain()
        self.rbac = SeafoodRBAC()
        self.batches = {}

    # --------------------------------------------------
    # STEP 1: FISHERMAN CREATES BATCH
    # --------------------------------------------------
    def create_batch(self, pid, batch_id, species, weight, location):
        if not self.rbac.can_perform_action(pid, "create_batch"):
            return {"success": False, "message": "Only Fisherman can create batches"}

        if batch_id in self.batches:
            return {"success": False, "message": "Batch already exists"}

        self.batches[batch_id] = {
            "species": species,
            "weight": weight,
            "current_owner": pid,
            "stage": "CREATED",
            "location": location
        }

        self.blockchain.add_block({
            "event": "BATCH_CREATED",
            "batch_id": batch_id,
            "from": "Ocean",
            "to": pid,
            "species": species,
            "weight": weight,
            "location": location,
            "details": "Batch created by fisherman",
            "performed_by": pid,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "message": "Batch created successfully"}

    # --------------------------------------------------
    # STEP 2: DISTRIBUTOR TRANSFER
    # --------------------------------------------------
    def transfer_ownership(self, pid, batch_id, new_owner, species, weight, location):
        if batch_id not in self.batches:
            return {"success": False, "message": "Batch does not exist"}

        if not self.rbac.can_perform_action(pid, "transfer_batch"):
            return {"success": False, "message": "Only Distributor can transfer ownership"}

        batch = self.batches[batch_id]

        if batch["stage"] != "CREATED":
            return {"success": False, "message": "Invalid workflow order"}

        if species != batch["species"]:
            return {"success": False, "message": "Species mismatch detected"}

        if weight != batch["weight"]:
            return {"success": False, "message": "Weight mismatch detected"}

        old_owner = batch["current_owner"]

        batch["current_owner"] = new_owner
        batch["location"] = location
        batch["stage"] = "TRANSFERRED"

        self.blockchain.add_block({
            "event": "OWNERSHIP_TRANSFER",
            "batch_id": batch_id,
            "from": old_owner,
            "to": new_owner,
            "species": species,
            "weight": weight,
            "location": location,
            "details": "Ownership transferred to distributor",
            "performed_by": pid,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "message": "Ownership transfer recorded"}

    # --------------------------------------------------
    # STEP 3: TRANSPORT UPDATE
    # --------------------------------------------------
    def update_transport(self, pid, batch_id, species, weight, location, details):
        if batch_id not in self.batches:
            return {"success": False, "message": "Batch does not exist"}

        if not self.rbac.can_perform_action(pid, "update_transport"):
            return {"success": False, "message": "Only Transporter can update transport"}

        batch = self.batches[batch_id]

        if batch["stage"] != "TRANSFERRED":
            return {"success": False, "message": "Invalid workflow order"}

        if species != batch["species"]:
            return {"success": False, "message": "Species mismatch detected"}

        if weight != batch["weight"]:
            return {"success": False, "message": "Weight mismatch detected"}

        batch["location"] = location
        batch["stage"] = "TRANSPORTED"

        self.blockchain.add_block({
            "event": "TRANSPORT_UPDATE",
            "batch_id": batch_id,
            "from": batch["current_owner"],
            "to": batch["current_owner"],
            "species": species,
            "weight": weight,
            "location": location,
            "details": details or "Transport update recorded",
            "performed_by": pid,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "message": "Transport update recorded"}

    # --------------------------------------------------
    # QUERY FULL TRACEABILITY
    # --------------------------------------------------
    def get_batch_history(self, batch_id):
        history = []
        for block in self.blockchain.chain:
            if block.data.get("batch_id") == batch_id:
                history.append(block.data)
        return history
