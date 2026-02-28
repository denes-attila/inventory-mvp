class Staff:
    def __init__(self, id, name, role):
        self.staff_id=id
        self.staff_name = name
        self.role = role

    def __str__(self):
        return self.staff_name

    def to_dict(self):
        return  {
                "id" :  self.staff_id,
                "name" : self.staff_name,
                "role" : self.role
            }   