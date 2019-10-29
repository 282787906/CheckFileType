class fileTemp:
    file_id = int
    name = str
    type = str
    hh_flag = str
    uid = str

    def __init__(self, uid, file_id, name, type, hh_flag):
        self.uid = uid
        self.file_id = file_id
        self.type = str(type)
        self.name = name
        self.hh_flag = hh_flag
