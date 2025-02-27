class EditorMemento:
    def __init__(self, text):
        self.text = text

class Editor:
    def __init__(self):
        self.text = ""

    def add_text(self, text):
        self.text += text

    def create_memento(self):
        return EditorMemento(self.text)
    
    def get_text(self): 
        return self.text
    
    def restore(self, memento):
        self.text = memento.text

class EditorMementoCareTaker:
    def __init__(self):
        self.mementos = [EditorMemento("")]

    def add_memento(self, memento):
        self.mementos.append(memento)

    def get_memento(self, index):
        return self.mementos[index]
    

obj = Editor()
care_taker = EditorMementoCareTaker()

obj.add_text("Hello")
care_taker.add_memento(obj.create_memento())
print(obj.get_text())

obj.add_text(" World")
care_taker.add_memento(obj.create_memento())
print(obj.get_text())


obj.restore(care_taker.get_memento(0))
print(obj.get_text())
obj.restore(care_taker.get_memento(1))
print(obj.get_text())
