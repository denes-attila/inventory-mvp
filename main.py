from inventory import InventoryManager
from database import initialize_db

initialize_db()

inventory = InventoryManager()

print("List of tasks" )
print('1 - list of staffs \n')
print('2 - Add staff member \n')
print('3 -Add device \n')
print("4 - List of devices \n")
print('5 - list available devices \n')
print('6 - assign device \n')
print('7 - unassign device \n')
print('8 - list devices for staff member \n')
print("9 - Delete member (staff)")
print("0 -  Exit")



chosen_task = None
while chosen_task != 0:
    inventory.load()
    chosen_task = int(input("Choose (1,2,3,4,5, 6, 7, 8, 9, 0): "))
    if chosen_task == 1:
        for s in inventory.staffs_list:
            print(s)
    elif chosen_task == 2:
        inventory.add_member()
        inventory.save()
    elif chosen_task == 3:
        inventory.add_device()
        inventory.save()
    elif chosen_task == 4:
        for d in inventory.devices_list:
            print(d)
    elif chosen_task == 5:
        for d in inventory.devices_list:
            if d.device_status == "available":
                print(d)
    elif chosen_task == 6:
        device_id = int(input("Give a device id: "))
        staff_id = int(input("Give a staff id: "))
        inventory.assign_device(device_id, staff_id)
        inventory.save()

    elif chosen_task == 7:
        device_id = int(input("Give a device id: "))
        inventory.unassign_device(device_id)
        inventory.save()
        
    elif chosen_task == 8:
        for f in inventory.staffs_list:
            print(f)
            for d in inventory.devices_list:
                if d.device_assigned_to == f:
                    print(d)
    

    elif chosen_task == 9:
        message = inventory.delete_member(int(input("Give the id for deleting member: ")))
        print(f"--->{message}")
        inventory.save()
inventory.conn.close()