

class GeneratorException(Exception):
    pass

class HintException(Exception):
    pass

class SettingsException(Exception):
    pass

class ValidationException(Exception):
    pass

class CantAssignItemException(Exception):
    pass

RandomizerExceptions = (GeneratorException,HintException,SettingsException,ValidationException)