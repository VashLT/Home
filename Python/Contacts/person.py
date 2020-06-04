
class Person():
    def __init__(self, name, phone_number, email, gener):
        self.__name = name
        self.__phone_number = phone_number
        self.__email = email
        self.__gener = gener
    
    def get_name(self):
        return self.__name

    def get_phoneNumber(self):
        return self.__phone_number
    
    def get_email(self):
        return self.__email
    
    def get_gener(self):
        return self.__gener
