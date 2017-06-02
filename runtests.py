# -*- coding: utf-8 -*-
"""
Entry point for Django tests.

This script will setup the basic configuration needed by Django.
"""

import sys
from os.path import abspath, dirname, join

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            'default': {
                'NAME': 'default',
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'cerberus_ac',
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        CERBERUS_DEFAULT_RESPONSE=False,
        CERBERUS_SKIP_IMPLICIT=False,
        CERBERUS_LOG_ACCESS=True,
        CERBERUS_LOG_PRIVILEGES=True,
        CERBERUS_LOG_HIERARCHY=True,
        CERBERUS_MAPPING=(
            ('cerberus_ac.models.Role',
             {'name': 'role', 'attr': 'role'}),
            ('test_cerberus_ac.FakeUser',
             {'name': 'FakeUser', 'attr': 'user resource'}),
            ('test_cerberus_ac.FakeGroup',
             {'name': 'FakeGroup', 'attr': 'group resource'}),
            ('test_cerberus_ac.FakeResource',
             {'name': 'FakeResource', 'attr': 'resource'}),
        )
    )

    try:
        import django
        sys.path.append(abspath(join(dirname(__file__), 'src')))

        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError('To fix this error, maybe run '
                      '`pip install -r requirements/test.txt`')


def run_tests(*test_args):
    """Discover and run tests."""
    if not test_args:
        test_args = ['tests']

    # Run tests
    runner = get_runner(settings)
    test_runner = runner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
