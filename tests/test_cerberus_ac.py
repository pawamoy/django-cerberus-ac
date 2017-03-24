# -*- coding: utf-8 -*-

"""Main test script."""

from django.test import TestCase

from django_fake_model import models as f

from cerberus_ac.models import Role, RoleMixin, RolePrivilege


class FakeUser(f.FakeModel, RoleMixin):
    """Fake user model."""


class FakeGroup(f.FakeModel, RoleMixin):
    """Fake group model."""


class FakeResource(f.FakeModel):
    """Fake resource model."""


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
        """Add users to self."""
        self.users = [FakeUser.objects.create() for _ in range(3)]

    def set_groups(self):
        """Add groups to self."""
        self.groups = [FakeGroup.objects.create() for _ in range(3)]

    def set_roles(self):
        """Add custom roles to self."""
        self.roles = [
            Role.objects.create(type='security'),
            Role.objects.create(type='audit'),
            Role.objects.create(type='data')
        ]

    def set_resources(self):
        """Add resources to self."""
        self.resources = [FakeResource.objects.create() for _ in range(3)]

    def set_role_hierarchy(self):
        """Set a role hierarchy."""
        self.users[0].join(self.groups[0])
        self.users[0].join(self.groups[1])
        self.groups[1].receive(self.users[1])
        self.roles[0].receive(self.users[0])
        self.roles[1].receive(self.users[1])
        self.roles[2].receive(self.users[2])

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

    def test_role_hierarchy_history(self):
        pass

    def set_role_privileges(self):
        """Set some role privileges."""
        RolePrivilege.allow('FakeUser', 1, 'do stuff', 'FakeResource', 1)
        RolePrivilege.allow('FakeUser', 2, 'do stuff', 'FakeResource', 2)
        RolePrivilege.allow('FakeUser', 3, 'do stuff', 'FakeResource', 3)
        RolePrivilege.deny('FakeUser', 1, 'do stuff', 'FakeResource', 2)
        RolePrivilege.deny('FakeUser', 2, 'do stuff', 'FakeResource', 3)
        RolePrivilege.deny('FakeUser', 3, 'do stuff', 'FakeResource', 1)

    def test_role_privileges(self):
        """Test the roles privileges."""
        # test direct explicit permission (allow, deny, default)
        assert self.users[0].can('do stuff', self.resources[0])
        assert self.users[1].can('do stuff', self.resources[1])
        assert self.users[2].can('do stuff', self.resources[2])
        assert not self.users[0].can('do stuff', self.resources[1])
        assert not self.users[1].can('do stuff', self.resources[2])
        assert not self.users[2].can('do stuff', self.resources[0])
        assert not self.users[0].can('do stuff', self.resources[2])
        assert not self.users[1].can('do stuff', self.resources[0])
        assert not self.users[2].can('do stuff', self.resources[1])
        # test indirect-1 explicit permission (allow, deny, default)
        # test indirect-2 explicit permission (allow, deny, default)
        # test direct overridden indirect-1 permission (allow, deny)
        # test direct overridden indirect-2 permission (allow, deny)
        # test clashing indirect-1 permissions
        # test clashing indirect-1-2 permissions (local > global)

    def test_role_privileges_history(self):
        pass

    def tearDown(self):
        """Tear down method."""
        pass
