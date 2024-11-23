class CommandManager:
    def __init__(self):
        self.history = []
        self.undo_stack = []
    
    def execute_command(self, command):
        """Execute a command and store it in history"""
        success, message = command.execute()
        if success:
            self.history.append(command)
            self.undo_stack = []  # Clear redo stack when new command is executed
        return success, message
    
    def undo_last_command(self):
        """Undo the last executed command"""
        if self.history:
            command = self.history.pop()
            success, message = command.undo()
            if success:
                self.undo_stack.append(command)
            return success, message
        return False, "No commands to undo"
    
    def redo_last_command(self):
        """Redo the last undone command"""
        if self.undo_stack:
            command = self.undo_stack.pop()
            success, message = command.execute()
            if success:
                self.history.append(command)
            return success, message
        return False, "No commands to redo"