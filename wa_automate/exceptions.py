class WAAutomateException(Exception):
    """Base exception class for WA_Automate application."""
    pass


class ConfigError(WAAutomateException):
    """Exception raised for errors in the configuration file or loading process."""
    pass


class DataLoaderError(WAAutomateException):
    """Exception raised when loading contact files (CSV/Excel/JSON) fails."""
    pass


class BrowserDriverError(WAAutomateException):
    """Exception raised when browser setup, control, or automation fails."""
    pass


class ValidationError(WAAutomateException):
    """Exception raised when phone numbers or input fields fail validation checks."""
    pass


class TemplateError(WAAutomateException):
    """Exception raised when formatting campaign message templates fails."""
    pass


class CampaignError(WAAutomateException):
    """Exception raised during the execution phase of a WhatsApp campaign."""
    pass
