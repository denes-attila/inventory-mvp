from staff import Staff
from device import Device
import json
import sqlite3




class InventoryManager:
    def __init__(self):
        self.devices_list = []
        self.staffs_list = []
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()

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
        self.cursor.execute(''' DELETE FROM staffs ''')
        self.cursor.execute(''' DELETE FROM devices '''
        )
        for staff in self.staffs_list:
            self.cursor.execute("""
            INSERT INTO staffs (id, name, role) VALUES (?,?,?)
        """, (staff.staff_id, staff.staff_name, staff.role))
        for device in self.devices_list:
            self.cursor.execute("""
            INSERT INTO devices (id, name, type, status, assigned_to) VALUES (?,?,?,?,?)
        """, (device.device_id, device.device_name, device.device_type, device.device_status, device.device_assigned_to.staff_id if device.device_assigned_to else None))
            
        self.conn.commit()
        

    def load(self):
        self.staffs_list = []
        self.devices_list = []
        try:
            self.cursor.execute("""SELECT * FROM staffs""")
            rows = self.cursor.fetchall()
            self.staffs_list = [Staff(row[0], row[1], row[2]) for row in  rows]

            self.cursor.execute("""SELECT * FROM devices""")
            d_rows = self.cursor.fetchall()
            for row in d_rows:
                d = Device(row[0], row[1], row[2])
                d.device_status = row[3]
                staff_id = row[4]
                if staff_id:
                    d.device_assigned_to = next((s for s in self.staffs_list if s.staff_id == staff_id), None)
                self.devices_list.append(d)

            
        except Exception as e:
            print(f"Hiba {e}")
