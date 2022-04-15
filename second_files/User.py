class User:
    def __init__(self, id=None, name="", acces=-1):
        self.id = id
        self.name = name
        self.acces = acces

    def getAcces(self):
        return self.acces

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def login(self, result):
        self.id = result[0]
        self.name = result[1]
        self.acces = result[3]

    def disconnect(self):
        self.id = None
        self.name = ""
        self.acces = -1

    def __str__(self):
        return "ID: " + str(self.id) + ", name: " + self.name + ", acces: " + str(self.acces)





