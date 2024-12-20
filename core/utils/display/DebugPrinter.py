class DebugPrinter:
    COLORS = {
        "reset": "\033[0m",
        "blue": "\033[1;34m",
        "green": "\033[1;32m",
        "yellow": "\033[1;33m",
        "cyan": "\033[1;36m",
        "magenta": "\033[1;35m",
        "white": "\033[1;37m",
        "red": "\033[1;31m",
        "gray": "\033[1;30m",
    }

    STATES = {
        "start": "START",
        "run": "RUN",
        "end": "END",
        "error": "ERROR",
        "info": "INFO",
        "debug": "DEBUG",
        "success": "SUCCESS",
        "warning": "WARNING",
    }

    CATEGORY = {
        "class": "CLASS",
        "attribute": "ATTRIBUTE",
        "method": "METHOD",
        "static_attribute": "STATIC_ATTRIBUTE",
        "static_method": "STATIC_METHOD",
        "function": "FUNCTION",
        "variable": "VARIABLE",
        "constant": "CONSTANT",
        "module": "MODULE",
        "message": "MESSAGE",
        "loop": "LOOP",	
        "condition": "CONDITION",
        "default": "DEFAULT",
        "exception": "EXCEPTION",
        "return": "RETURN",
    }

    EVOLUTION = {
        "creation": "CREATION",
        "initialization": "INITIALIZATION",
        "update": "UPDATE",
        "delete": "DELETE",
        "check": "CHECK",
        "compare": "COMPARE",
        "conversion": "CONVERSION",
        "validation": "VALIDATION",
    }

    _display = False  # Variable de classe pour activer/désactiver l'affichage

    @classmethod
    def set_display(cls, value: bool):
        """Change le statut de l'affichage."""
        if not isinstance(value, bool):
            raise TypeError(f"Expected boolean value, got {type(value)}.")
        cls._display = value


    @classmethod
    def header(cls, class_name, method_name, state):
        """Affiche l'en-tête de la classe et de la méthode."""
        return f"{cls.COLORS['blue']}CLASS {class_name}{cls.COLORS['reset']} " \
               f"{cls.COLORS['green']}METHOD {method_name}{cls.COLORS['reset']} " \
               f"{cls.COLORS['yellow']}STATE: {state}{cls.COLORS['reset']}"

    @classmethod
    def variable(cls, var_name, var_type, var_value, additional_info=None):
        """Affiche les détails d'une variable."""
        output = (
            f"{cls.COLORS['cyan']}CREATION VARIABLE {var_name}{cls.COLORS['reset']} "
            f"{cls.COLORS['magenta']}TYPE {var_type}{cls.COLORS['reset']} "
            f"{cls.COLORS['white']}{var_value}{cls.COLORS['reset']}"
        )
        if additional_info:
            output += " :\n"
            for key, value in additional_info.items():
                output += (
                    f"    {cls.COLORS['yellow']}{key}{cls.COLORS['reset']} "
                    f"= {cls.COLORS['white']}{value}{cls.COLORS['reset']}\n"
                )
        return output
    
    def loop(cls, loop_name, loop_type, loop_value):
        """Affiche les détails d'une boucle."""
        return (
            f"{cls.COLORS['cyan']}LOOP {loop_name}{cls.COLORS['reset']} "
            f"{cls.COLORS['magenta']}TYPE {loop_type}{cls.COLORS['reset']} "
            f"{cls.COLORS['white']}{loop_value}{cls.COLORS['reset']}"
        )
        
        
    def condition(cls, condition_name, condition_type, condition_value):
        """Affiche les détails d'une condition."""
        return (
            f"{cls.COLORS['cyan']}CONDITION {condition_name}{cls.COLORS['reset']} "
            f"{cls.COLORS['magenta']}TYPE {condition_type}{cls.COLORS['reset']} "
            f"{cls.COLORS['white']}{condition_value}{cls.COLORS['reset']}"
        )
        
    def exception(cls, exception_name, exception_type, exception_value):
        """Affiche les détails d'une exception."""
        return (
            f"{cls.COLORS['red']}EXCEPTION {exception_name}{cls.COLORS['reset']} "
            f"{cls.COLORS['red']}TYPE {exception_type}{cls.COLORS['reset']} "
            f"{cls.COLORS['white']}{exception_value}{cls.COLORS['reset']}"
        )
        
    @classmethod
    def message(cls, msg, color="white"):
        """Affiche un message général de débogage."""
        color_code = cls.COLORS.get(color, cls.COLORS["white"])
        return f"{color_code}{msg}{cls.COLORS['reset']}"

    @classmethod
    def debug(cls, *messages):
        """Affiche un groupe de messages si l'affichage est activé."""
        if cls._display:
            for message in messages:
                print(message)


