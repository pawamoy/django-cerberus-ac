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
        self.ACCESS_CONTROL_DEFAULT_RESPONSE = None

    def load(self):
        """Load every settings in self."""
        self.ACCESS_CONTROL_DEFAULT_RESPONSE = AppSettings.get_default_response()  # noqa

    @staticmethod
    def check():
        """Run every check method for settings."""
        AppSettings.check_default_response()

    @staticmethod
    def check_default_response():
        """Check the value of given default response setting."""
        default_response = AppSettings.get_default_response()
        if not isinstance(default_response, bool):
            raise ValueError('DEFAULT_RESPONSE must be True or False')

    @staticmethod
    def get_default_response():
        """Return default response setting."""
        return getattr(settings, 'ACCESS_CONTROL_DEFAULT_RESPONSE', False)


AppSettings.check()
