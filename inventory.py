from staff import Staff
from device import Device
import json

class InventoryManager:
    def __init__(self):
        self.devices_list = []
        self.staffs_list = []

    def add_member(self):
        new_member = Staff(int(input("Id: ")), input("Name: " ), input("Role: "))
        self.staffs_list.append(new_member)

    def add_device(self):
        new_device = Device(int(input("Id: ")), input("Name: " ), input("Type: "))
        self.devices_list.append(new_device)

    def delete_member(self, id):
        
        found_staff = next((s for s in self.staffs_list if s.staff_id == id), None)

        if not found_staff:
            return "No such a staff"
        
        has_device = any(d.device_assigned_to == found_staff for d in self.devices_list)

        if has_device:
            return "Not deletable: has device"
                
        self.staffs_list.remove(found_staff)
        return "Staff removed successfully"
    
    
    def assign_device(self, dev_id, staff_id):
        
        target_device = next((d for d in self.devices_list if d.device_id == dev_id), None)
        target_staff = next((s for s in self.staffs_list if s.staff_id == staff_id), None)

        if target_device and target_staff:
            if target_device.device_status != "available":
                print(f"Device {target_device.device_name} is not available")
            else:
                target_device.assign(target_staff)
                print(f"Device successfully assigned: {target_device}")
        else:
            print("error: device or staff not reasonable")


    def unassign_device(self, dev_id):
        target_device = next((d for d in self.devices_list if d.device_id == dev_id), None)
        if target_device:
            if target_device.device_status == "assigned":
                target_device.unassign()
            else:
                print(f"The chosen device ({target_device.device_name}) is not assigned")
        else:
            print("Error. Device not found.")

    
    def get_available_devices(self):
        return [d for d in self.devices_list if d.device_assigned_to is None]

    def get_devices_for_staff(self, staff):
        return [d for d in self.devices_list if d.device_assigned_to == staff]

    def save(self):
        data = {
            "staffs":[staff.to_dict() for staff in self.staffs_list],
            "devices":[device.to_dict() for device in self.devices_list]
        }
        with open("inventory.json", "w") as f:
            json.dump(data, f)

    def load(self):
        self.staffs_list = []
        self.devices_list = []
        try:
            with open("inventory.json") as json_file:
                items = json.load(json_file)
                self.staffs_list = [Staff(item["id"], item["name"], item["role"]) for item in  items["staffs"]]
                for item in items["devices"]:
                    d = Device(item["id"], item["name"], item["type"])
                    d.device_status = item["status"]
                    staff_id = item["assigned_to"]
                    if staff_id:
                        d.device_assigned_to = next((s for s in self.staffs_list if s.staff_id == staff_id), None)
                    self.devices_list.append(d)
        except FileNotFoundError:
            pass

        except json.JSONDecodeError:
            pass

