from datetime import datetime
from lib.utils.colors import TC

class Logger:
    """Custom Logger class for formatted console output with color coding.
    This class provides static and class methods for logging messages with different
    severity levels (DEBUG, INFO, WARN, ERROR, SUCCESS) and custom types. Each message
    is formatted with timestamp, log level, and optional function name.
    Class Methods:
        success(message: str, func_name: str = None) -> None:
            Log a success message in green color.
        error(message: str, func_name: str = None) -> None:
            Log an error message in red color.
        warn(message: str, func_name: str = None) -> None:
            Log a warning message in yellow color.
        info(message: str, func_name: str = None) -> None:
            Log an info message in blue color.
        debug(message: str, func_name: str = None) -> None:
            Log a debug message in magenta color.
        custom(type_: str, message: str, func_name: str = None) -> None:
            Log a custom message with cyan color for type.
    Static Methods:
        _get_time_for_log_format() -> str:
            Get current timestamp in format "YYYY-MM-DD HH:MM:SS".
        _log(type_: str, message: str, func_name: str = None) -> None:
            Internal method to handle log message formatting and output.
    Format:
        [TIMESTAMP] [LOG_LEVEL] funcName: {func_name}: MESSAGE
    Colors:
        - SUCCESS: Green
        - ERROR: Red
        - WARN: Yellow
        - INFO: Blue
        - DEBUG: Magenta
        - CUSTOM: Cyan
    """
    @staticmethod
    def _get_time_for_log_format() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _log(type_: str, message: str, func_name: str = None) -> None:
        color_map = {
            "DEBUG": TC.M,
            "WARN": TC.BY,
            "ERROR": TC.R,
            "INFO": TC.B,
            "SUCCESS": TC.G
        }
        
        color = color_map.get(type_, TC.reset)
        current_time = Logger._get_time_for_log_format()
        function_name = f"funcName: {func_name}" if func_name else ""
        
        log_message = f"{TC.dim}[{current_time}]{TC.reset} {color}[{type_}]{TC.reset} {function_name}: {message}"
        
        if type_ in ["ERROR", "WARN"]:
            print(log_message)
        elif type_ == "INFO":
            print(log_message)
        else:
            print(log_message)

    @classmethod
    def success(cls, message: str, func_name: str = None) -> None:
        cls._log("SUCCESS", message, func_name)

    @classmethod
    def error(cls, message: str, func_name: str = None) -> None:
        cls._log("ERROR", message, func_name)

    @classmethod
    def warn(cls, message: str, func_name: str = None) -> None:
        cls._log("WARN", message, func_name)

    @classmethod
    def info(cls, message: str, func_name: str = None) -> None:
        cls._log("INFO", message, func_name)

    @classmethod
    def debug(cls, message: str, func_name: str = None) -> None:
        cls._log("DEBUG", message, func_name)

    @classmethod
    def custom(cls, type_: str, message: str, func_name: str = None) -> None:
        current_time = cls._get_time_for_log_format()
        function_name = f"funcName: {func_name}" if func_name else ""
        print(f"{TC.dim}[{current_time}]{TC.reset} {TC.C}[{type_}]{TC.reset} {function_name}: {message}")
