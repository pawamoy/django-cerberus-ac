=======================
Cerberus Access Control
=======================

.. start-badges


|travis|
|codacygrade|
|codacycoverage|
|version|
|wheel|
|pyup|
|gitter|


.. |travis| image:: https://travis-ci.org/Deavelleye/dj-CerberusAC.svg?branch=master
    :target: https://travis-ci.org/Deavelleye/dj-CerberusAC/
    :alt: Travis-CI Build Status

.. |codacygrade| image:: https://api.codacy.com/project/badge/Grade/9317db72ae5b4616a12b962ae21fe169
    :target: https://www.codacy.com/app/Deavelleye/dj-CerberusAC/dashboard
    :alt: Codacy Code Quality Status

.. |codacycoverage| image:: https://api.codacy.com/project/badge/Coverage/9317db72ae5b4616a12b962ae21fe169
    :target: https://www.codacy.com/app/Deavelleye/dj-CerberusAC/dashboard
    :alt: Codacy Code Coverage

.. |pyup| image:: https://pyup.io/repos/github/Deavelleye/dj-CerberusAC/shield.svg
    :target: https://pyup.io/repos/github/Deavelleye/dj-CerberusAC/
    :alt: Updates

.. |version| image:: https://img.shields.io/pypi/v/django-cerberus-ac.svg?style=flat
    :target: https://pypi.python.org/pypi/django-cerberus-ac/
    :alt: PyPI Package latest release

.. |wheel| image:: https://img.shields.io/pypi/wheel/django-cerberus-ac.svg?style=flat
    :target: https://pypi.python.org/pypi/django-cerberus-ac/
    :alt: PyPI Wheel

.. |gitter| image:: https://badges.gitter.im/dj-CerberusAC/Lobby.svg
    :target: https://gitter.im/dj-CerberusAC/Lobby
    :alt: Join the chat at https://gitter.im/dj-CerberusAC/Lobby


.. end-badges

Django Ontology Based Access Control Module.

License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    pip install django-cerberus-ac

Usage
=====

In your main project's ``__init__.py`` , create 2 functions to pass the list of resources available and list of roles.


Documentation
=============

`On ReadTheDocs`_

.. _`On ReadTheDocs`: http://dj-cerberusac.readthedocs.io/

Development
===========

To run all the tests: ``tox``
