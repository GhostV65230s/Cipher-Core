# rbac.py

ROLES_PERMISSIONS = {
    "Fisherman": ["create_batch"],
    "Distributor": ["transfer_batch"],
    "Transporter": ["update_transport"],
    "Retailer": ["receive_delivery"]
}

PARTICIPANTS = {
    "F001": {"role": "Fisherman"},
    "D001": {"role": "Distributor"},
    "T001": {"role": "Transporter"},
    "R001": {"role": "Retailer"},
}

class SeafoodRBAC:
    def __init__(self):
        self.participants = PARTICIPANTS

    def can_perform_action(self, participant_id, action):
        participant = self.participants.get(participant_id)
        if not participant:
            return False

        role = participant["role"]
        return action in ROLES_PERMISSIONS.get(role, [])
