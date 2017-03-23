# -*- coding: utf-8 -*-

"""Main test script."""

from django.test import TestCase
from django_fake_model import models as f

from cerberus_ac.models import (
    Role, RoleMixin, RolePrivilege, AccessHistory,
    PrivilegeHistory)


class FakeUser(f.FakeModel, RoleMixin):
    pass


class FakeGroup(f.FakeModel, RoleMixin):
    pass


class FakeResource(f.FakeModel):
    pass


@FakeUser.fake_me
@FakeGroup.fake_me
@FakeResource.fake_me
class MainTestCase(TestCase):
    """Main Django test case."""

    def setUp(self):
        """Setup method."""
        self.set_users()
        self.set_groups()
        self.set_roles()
        self.set_resources()
        self.set_role_hierarchy()
        self.set_role_privileges()

    def set_users(self):
        self.users = [FakeUser.objects.create() for _ in range(3)]

    def set_groups(self):
        self.groups = [FakeGroup.objects.create() for _ in range(3)]

    def set_roles(self):
        self.roles = [
            Role.objects.create(type='security'),
            Role.objects.create(type='audit'),
            Role.objects.create(type='data')
        ]

    def set_resources(self):
        self.resources = [FakeResource.objects.create() for _ in range(3)]

    def set_role_hierarchy(self):
        self.users[0].join(self.groups[0])
        self.users[0].join(self.groups[1])
        self.groups[1].receive(self.users[1])
        self.roles[0].receive(self.users[0])
        self.roles[1].receive(self.users[1])
        self.roles[2].receive(self.users[2])

    def set_role_privileges(self):
        RolePrivilege.allow('FakeUser', 1, 'do stuff', 'FakeResource', 1)
        RolePrivilege.allow('FakeUser', 2, 'do stuff', 'FakeResource', 2)
        RolePrivilege.allow('FakeUser', 3, 'do stuff', 'FakeResource', 3)
        RolePrivilege.deny('FakeUser', 1, 'do stuff', 'FakeResource', 2)
        RolePrivilege.deny('FakeUser', 2, 'do stuff', 'FakeResource', 3)
        RolePrivilege.deny('FakeUser', 3, 'do stuff', 'FakeResource', 1)

    def test_role_hierarchy(self):
        """Role hierarchy test method."""
        assert self.users[0].is_child_of(self.groups[0])
        assert self.users[0].is_child_of(self.groups[1])
        assert not self.users[0].is_child_of(self.groups[2])
        assert set(self.groups[1].children()) == {
            ('FakeUser', 1), ('FakeUser', 2)}
        assert self.roles[0].is_parent_of(self.users[0])
        assert self.roles[1].is_parent_of(self.users[1])
        assert self.roles[2].is_parent_of(self.users[2])
        assert set(self.users[0].parents()) == {
            ('FakeGroup', 1), ('FakeGroup', 2), ('security', 1)}

    def test_role_privileges(self):
        # test direct explicit permission (allow, deny, default)
        # test indirect-1 explicit permission (allow, deny, default)
        # test indirect-2 explicit permission (allow, deny, default)
        # test direct overridden indirect-1 permission (allow, deny)
        # test direct overridden indirect-2 permission (allow, deny)
        # test clashing indirect-1 permissions
        # test clashing indirect-1-2 permissions (local > global)
        pass

    def tearDown(self):
        """Tear down method."""
        pass
