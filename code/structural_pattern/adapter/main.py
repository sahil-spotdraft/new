# target
class TextLogger:
    def log(self, message: str):
        raise NotImplementedError("This method should be overridden")

# adaptee
import json

class JsonLogger:
    def log_json(self, message: dict):
        print("Logging JSON:", json.dumps(message))

# adapter
class JsonToTextLoggerAdapter(TextLogger):
    def __init__(self, json_logger: JsonLogger):
        self.json_logger = json_logger

    def log(self, message: str):
        # Convert plain text message to JSON format
        message_json = {"message": message}
        self.json_logger.log_json(message_json)

# client code
# Client expects a TextLogger
def client_code(logger: TextLogger):
    logger.log("Adapter pattern example")

# Using the adapter
json_logger = JsonLogger()
adapter = JsonToTextLoggerAdapter(json_logger)

# Now we can use the JSON logger as if it's a TextLogger
client_code(adapter)
