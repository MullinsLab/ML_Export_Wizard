from django.conf import settings

import logging
log = logging.getLogger(settings.ML_EXPORT_WIZARD['Logger'])

import inspect

class LoggingException(Exception):
    """ Class to inherit if we want exceptions logged """
    def __init__(self, message: str=''):
        message = f"{inspect.stack()[1].filename}:{inspect.stack()[1].lineno} ({inspect.stack()[1].function}) {message}"
        
        if settings.ML_EXPORT_WIZARD['Log_Exceptions']:
            log.warn(message)
        
        self.message = message

    def __str__(self) -> str:
        return self.message
    

class MLExportWizardFieldNotFound(LoggingException):
    """ A field (or app or model) was requested that doesn't exist """

class MLExportWizardQueryExecuting(LoggingException):
    """ The query is executing which is preventing its structure from changing """

class MLExportWizardQueryNotExecuted(LoggingException):
    """ The query has not been executed yet """

class MLExportWizardExporterNotFound(LoggingException):
    """ The exporter was not found """