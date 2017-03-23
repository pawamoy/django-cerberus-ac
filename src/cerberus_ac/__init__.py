# -*- coding: utf-8 -*-

r"""Cerberus Access Control package."""

from django.conf import settings

__version__ = '0.1.0'


# TODO: app settings for skip implicit and log default values
class AppSettings(object):
    """
    Application settings class.

    This class provides static getters for each setting, and also an instance
    ``load`` method to load every setting in an instance.
    """

    def __init__(self):
        """Init method."""
        self.CERBERUS_DEFAULT_RESPONSE = None
        self.CERBERUS_SKIP_IMPLICIT = None

    def load(self):
        """Load every settings in self."""
        self.CERBERUS_DEFAULT_RESPONSE = AppSettings.get_default_response()
        self.CERBERUS_SKIP_IMPLICIT = AppSettings.get_skip_implicit()

    @staticmethod
    def check():
        """Run every check method for settings."""
        AppSettings.check_default_response()
        AppSettings.check_skip_implicit()

    @staticmethod
    def check_default_response():
        """Check the value of given default response setting."""
        default_response = AppSettings.get_default_response()
        if not isinstance(default_response, bool):
            raise ValueError('DEFAULT_RESPONSE must be True or False')

    @staticmethod
    def get_default_response():
        """Return default response setting."""
        return getattr(settings, 'CERBERUS_DEFAULT_RESPONSE', False)

    @staticmethod
    def check_skip_implicit():
        """Check the value of given skip implicit setting."""
        skip_implicit = AppSettings.get_skip_implicit()
        if not isinstance(skip_implicit, bool):
            raise ValueError('SKIP_IMPLICIT must be True or False')

    @staticmethod
    def get_skip_implicit():
        """Return skip implicit setting."""
        return getattr(settings, 'CERBERUS_SKIP_IMPLICIT', False)

    @staticmethod
    def check_log_access():
        """Check the value of given log access setting."""
        log_access = AppSettings.get_log_access()
        if not isinstance(log_access, bool):
            raise ValueError('LOG_ACCESS must be True or False')

    @staticmethod
    def get_log_access():
        """Return log access setting."""
        return getattr(settings, 'CERBERUS_LOG_ACCESS', True)


AppSettings.check()
