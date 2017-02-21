# -*- coding: utf-8 -*-

"""Main test script."""



from django.test import TestCase

import cerberus_ac


class MainTestCase(TestCase):
    """Main Django test case."""

    def setUp(self):
        """Setup method."""
        pass

    def test_main(self):
        """Main test method."""
        assert cerberus_ac

    def tearDown(self):
        """Tear down method."""
        pass
