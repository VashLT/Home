from person import Person

class User(Person):
    def __init__(self, user_id, password):
        super().__init__()
        self.__id = user_id
        self.__password = password
        self.__contacts = []

    def get_id():
        return self.__id
    
    def add_contact(self, name, phone_number):
        pass

    def delete_contact(self, name, phone_number):
        pass

    def show_contacts(self):
        if self.__contacts:
            contacts = self.__contacts
            for contact in contacts:
                print('')
