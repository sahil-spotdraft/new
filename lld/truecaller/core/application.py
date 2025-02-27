import abc


class CommandLineApplication(abc.ABC):
    @classmethod
    def _run_command(cls, command: str, **kwargs):
        if not hasattr(cls, "commands") or command not in cls.commands:
            print("Command not found")
            return

        command_info = cls.commands[command]
        converted_kwargs = {}

        for param_name, param_type in command_info.items():
            if param_name == "method" or param_name == "help":
                continue
            if param_name not in kwargs:
                print(f"Missing required argument: {param_name}")
                return
            try:
                converted_kwargs[param_name] = (
                    kwargs[param_name] 
                    if param_type == str
                    else param_type(kwargs[param_name])
                )
            except ValueError:
                print(f"Invalid value for argument {param_name}: {kwargs[param_name]}")
                return

        response = command_info["method"](**converted_kwargs)
        if response:
            print(response)

    @classmethod
    def _read_command(cls, raw_command: str):
        command, val = raw_command.split(" ")
        if not command:
            raise ValueError("Invalid comamnd")
        kwargs = {}
        if val:
            try:
                kwargs = dict(item.split("=") for item in val.split(","))
            except Exception:
                raise ValueError("Invalid comamnd")
        cls._run_command(command, **kwargs)

    @classmethod
    def start_cli(cls):
        help_texts = []
        if hasattr(cls, "commands"):
            help_texts = [
                command["help"]
                for command in getattr(cls, "commands", {}).values()
            ]

        while True:
            print("Enter command (type 'help' for available commands): ")
            command = input().strip().lower()

            if command == 'help':
                print("Available commands:")
                print("- help: Display available commands")
                print("- quit: Exit the program")
                for help in help_texts:
                    print(help)
                # Add more commands and their descriptions as needed

            elif command in ['quit', 'q', 'c']:
                print("Exiting program...")
                break

            elif command.split(" ")[0] in getattr(cls, "commands", {}):
                cls._read_command(command)

            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")