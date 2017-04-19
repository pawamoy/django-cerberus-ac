=========
Changelog
=========

0.1.6 (2017-04-19)
==================

- Finish implementation of edit privileges page (efficient below 1000*1000 matrices).

0.1.5 (2017-04-18)
==================

- Improve admin display.
- Add allow_update_own_privileges setting.
- Improve ``instance_from_`` method.
- Add ``skip_implicit`` and ``log`` kwargs on ``can`` method.
- Fix role hierarchy chart, use ``allow_own_update`` setting.
- Put back ``setting_prefix``.
- Add ``django-app-settings`` dependency, remove ``autowidth`` from data-table.
- Move access to objects into get to avoid migrate errors.
- Remove Github pages configuration file.
- Update django from 1.10.6 to 1.11.
- Fix migrations (missing ``__init__.py``).

0.1.4 (2017-04-10)
==================

- Implement Ajax call with notification.
- Interface ``no_datatable`` template with backend.
- Set namespace to cerberus, improve consistency.
- Match application name in breadcrumbs.
- Move application settings into ``apps`` module.
- Change IDs from ``int`` to ``str``.
- Add migration file, avoid loading role instances at start-up.
- Change mapping setting.
- Register models in admin.
- Fix unique constraint with integers default 0.

0.1.3 (2017-04-04)
==================

* Admin classes added for separation of privileges.
* Models updated.

0.1.2 (2017-04-03)
==================

* Added views, templates, and models for testing.
* Changed Bootstrap version from 3.3.1 to 2.3.1  and JQuery 3.1.1 to 2.1.1.

0.1.1 (2017-02-21)
==================

* Alpha release on PyPI.

