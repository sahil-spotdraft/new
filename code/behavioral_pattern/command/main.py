# Command
class Command:
    def execute(self):
        pass


# Concrete commands
class TurnOnCommand(Command):
    def __init__(self, device: "Device"):
        self.device = device

    def execute(self):
        self.device.on()

class TurnOffCommand(Command):
    def __init__(self, device: "Device"):
        self.device = device

    def execute(self):
        self.device.off()

class SetVolumeUpCommand(Command):
    def __init__(self, stereo: "Stereo"):
        self.stereo = stereo
    
    def execute(self):
        self.stereo.set_volume(2)

class SetVolumeDownCommand(Command):
    def __init__(self, stereo: "Stereo"):
        self.stereo = stereo
    
    def execute(self):
        self.stereo.set_volume(-2)

class ChangeChannelCommand(Command):
    def __init__(self, tv: "Tv"):
        self.tv = tv

    def execute(self):
        self.tv.change_channel()
        

# Receiver(Devies)
class Device:
    def on(self):
        pass

    def off(self):
        pass

    def set_volume(self, vol):
        pass

    def change_channel(self):
        pass

class Stereo(Device):
    def on(self):
        print("Stereo on")
    
    def off(self):
        print("Stereo off")

    def set_volume(self, vol):
        print("Stereo " + vol)

class Tv(Device):
    def on(self):
        print("Tv on")
    
    def off(self):
        print("Tv off")

    def change_channel(self):
        print("Tv channel change")


# Invoker
class RemoteController:
    def __init__(self):
        self._command: Command = None

    def set_command(self, command: Command):
        self._command = command

    def perform_command(self):
        self._command.execute()


# Client
remote = RemoteController()
remote.set_command(TurnOffCommand(Tv()))
remote.perform_command()
remote.set_command(TurnOnCommand(Stereo()))
remote.perform_command()



