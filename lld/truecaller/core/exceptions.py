class Raise404(Exception):
    def __init__(self, message="Object not found"):
        self.message = message
        super().__init__(self.message)
