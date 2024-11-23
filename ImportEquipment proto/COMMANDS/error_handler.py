class CommandError(Exception):
    """Custom error class for command operations"""
    def __init__(self, message, command=None, function=None, args=None):
        self.message = message
        self.command = command
        self.function = function
        self.args = args
        
    def __str__(self):
        error_msg = [
            "\n=== Command Error ===",
            f"Error: {self.message}"
        ]
        
        if self.command:
            error_msg.append(f"Command: {self.command}")
            
        if self.args:
            error_msg.append(f"Arguments: {self.args}")
            
        if self.function:
            error_msg.append(f"Failed in: {self.function}")
            
        error_msg.append("==================")
        return "\n".join(error_msg)

def command_error_handler(func):
    """Decorator for handling command errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CommandError as e:
            return str(e)
        except Exception as e:
            # Get the command context from the first argument (self) if available
            command_context = ""
            if args and hasattr(args[0], 'current_command'):
                command_context = args[0].current_command
            
            return str(CommandError(
                message=str(e),
                command=command_context,
                function=f"{func.__qualname__}",
                args=args[1:] if args else None
            ))
    return wrapper