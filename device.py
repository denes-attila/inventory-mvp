class Device:
    def __init__(self, id, name, device_type, ):
        self.device_id = id
        self.device_name = name
        self.device_type = device_type
        self.device_status = "available"
        self.device_assigned_to = None

    def assign(self, staff):
        self.device_assigned_to = staff
        self.device_status = "assigned"

    def unassign(self):
        self.device_assigned_to = None
        self.device_status = "available"

    def __str__(self):
        if self.device_assigned_to:
            return f"{self.device_name} ({self.device_type}) is assigned to {self.device_assigned_to}"
        else:
            return f"{self.device_name} ({self.device_type}) is available"
        


    def to_dict (self):
        return {
            "id": self.device_id,
            "name": self.device_name,
            "type": self.device_type,
            "status": self.device_status,
            "assigned_to": self.device_assigned_to.staff_id if self.device_assigned_to else None,
        }