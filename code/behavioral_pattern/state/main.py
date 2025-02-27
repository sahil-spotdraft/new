class DocumentState:
    def visibility(self, user_type):
        pass

class Draft(DocumentState):
    def visibility(self, user_type):
        if user_type == "author":
            return True
        elif user_type == "client":
            return False
        
class Publish(DocumentState):
    def visibility(self, user_type):
        if user_type == "author":
            return True
        elif user_type == "client":
            return True

class Document:
    def __init__(self):
        self._state = Draft()

    def publish(self):
        self._state = Publish()

    def draft(self):
        self._state = Draft()

    def read(self, user_type):
        if self._state.visibility(user_type):
            print("Document loading...")
        else:
            print("Document not found")

obj = Document()
obj.read("client")
obj.publish()
obj.read("client")