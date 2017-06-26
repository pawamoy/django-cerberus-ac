# -*- coding: utf-8 -*-

"""cerberus_ac plugins module."""

try:
    from archan import Provider, Argument, DSM as ArchanDSM

    class Privileges(Provider):
        """Dependenpy provider for Archan."""

        identifier = 'cerberus_ac.Privileges'
        name = 'Privileges'
        description = 'Provide matrix data about privileges in an access ' \
            'control scheme.'

        def get_dsm(self):
            """
            Provide matrix data about privileges in an access control scheme.

            Returns:
                archan.DSM: instance of archan DSM.
            """
            data = []
            keys = []
            return ArchanDSM(data=data, entities=keys)

except ImportError:
    class Privileges(object):
        """Empty cerberus_ac provider."""
