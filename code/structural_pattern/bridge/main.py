from abc import ABC, abstractmethod

class CommunicationAPI(ABC):
    @abstractmethod
    def send_data(self, data):
        pass

class BluetoothCommunication(CommunicationAPI):
    def send_data(self, data):
        print(f"Sending data '{data}' via Bluetooth")

class WiFiCommunication(CommunicationAPI):
    def send_data(self, data):
        print(f"Sending data '{data}' via WiFi")

class Device:
    def __init__(self, communication_api):
        self.communication_api = communication_api

    @abstractmethod
    def communicate(self, data):
        pass

class Phone(Device):
    def communicate(self, data):
        print("Communicating via Phone:")
        self.communication_api.send_data(data)

class Speaker(Device):
    def communicate(self, data):
        print("Communicating via Speaker:")
        self.communication_api.send_data(data)

# Client code
if __name__ == "__main__":
    bluetooth_communication = BluetoothCommunication()
    wifi_communication = WiFiCommunication()

    phone = Phone(bluetooth_communication)
    speaker = Speaker(wifi_communication)

    phone.communicate("Hello, phone!")
    speaker.communicate("Hi, speaker!")