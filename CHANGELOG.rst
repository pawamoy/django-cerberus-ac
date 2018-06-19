=========
Changelog
=========

0.2.5 (2018-06-19)
==================

- Improve performance by getting conveyors/heirs iteratively instead of recursively
  (database requests number drastically reduced).

0.2.4 (2018-01-18)
==================

- Fix missing ``django-suit-dashboard`` in ``setup.py``.
- Fix usage of ``django-app-settings`` 0.3.0 in ``urls.py``.

0.2.3 (2017-12-11)
==================

- Fix mapping setting for ``django-app-settings`` 0.3.0.

0.2.2 (2017-12-11)
==================

- Update to support ``django-app-settings`` 0.3.0.

0.2.1 (2017-11-08)
==================

- Fix ``save() prohibited to prevent data loss due to unsaved related object 'reference'`` error in admin ``save_model``.

0.2.0 (2017-07-03)
==================

- Override ``save_models`` admin methods to add user in history records.
- Add and rename methods in ``RoleMixin``.
- Fix mapping setting check function.
- Implement implicit authorization.
- Add Science/Research classifier.
- Fix bug when id cannot be coerced to right type.
- Add migration 2.
- Improve ``RolePrivilege`` admin.
- Add drag and zoom to role hierarchy graph.
- Update initial migration to reflect code.

0.1.7 (2017-04-19)
==================

- Add ``d3.min.js`` as a static asset to enable it in SSL context.

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
