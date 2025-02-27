class Character:
    def __init__(self, ch, font_name, font_size, is_bold, is_italic):
        self.ch = ch
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic

    def __str__(self):
        return (
            f"{self.ch}-{self.font_name}-{self.font_size}{'-b' if self.is_bold else ''}{'-i' if self.is_italic else ''}"
        )

class CharacterFactory:
    def __init__(self):
        self._chars = []

    def add_character(self, row, col, ch, font_name, font_size, is_bold, is_italic):
        while len(self._chars) <= row:
            self._chars.append([])
        self._chars[row].insert(
            min(col, len(self._chars[row])), 
            Character(ch, font_name, font_size, is_bold, is_italic)
        )

    def get_style(self, row, col):
        if not self._is_valid(row, col): return ""
        return str(self._chars[row][col])
    
    def read_line(self, row):
        if not self._is_valid(row): return ""
        res = ""
        for char in self._chars[row]:
            res += char.ch
        return res
    
    def delete_character(self, row, col):
        if not self._is_valid(row, col):
            return False
        self._chars[row].pop(col)
        return True

    def _is_valid(self, row, col = None):
        return 0 <= row < len(self._chars) and 0 <= col < len(self._chars[row]) if col else True

class TextEditor:
    def __init__(self):
        self.factory = CharacterFactory()

    def add_character(self, row, col, ch, font_name, font_size, is_bold, is_italic):
        self.factory.add_character(row, col, ch, font_name, font_size, is_bold, is_italic)
    
    def get_style(self, row, col):
        return self.factory.get_style(row, col)

    def read_line(self, row):
        return self.factory.read_line(row)

    def delete_character(self, row, col):
        return self.factory.delete_character(row, col)
    

obj = TextEditor()
obj.add_character(0, 0, 'g', 'Cambria', 17, True, True)
obj.add_character(1, 0, 'y', 'Century Gothic', 14, True, True)
obj.add_character(1, 1, 'h', 'Courier New', 22, False, False)
obj.add_character(1, 2, 'y', 'Georgia', 14, False, False)

print(obj.get_style(0,0))
# returns 'g-Cambria-17-b-i'
print(obj.read_line(0))
# returns 'g'
obj.add_character(0, 0, 'q', 'Arial', 21, False, True)
print(obj.read_line(0))
# returns 'qg'

print(obj.read_line(1))
# returns 'yhy'
print(obj.delete_character(1, 1))
# returns true
print(obj.read_line(1))
# returns 'yy'
print(obj.delete_character(1, 4))
# returns false


# g-Cambria-17-b-i
# g
# qg
# yhy
# True
# yy
# False