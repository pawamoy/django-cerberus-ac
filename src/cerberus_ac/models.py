# -*- coding: utf-8 -*-

"""
Models and mixins for access control.

- RoleMixin
- Role
- RoleHierarchy
- RolePrivilege
- PrivilegeHistory
- AccessHistory
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import AppSettings


class RoleMixin(object):
    """
    Mixin for Role models / classes.

    This mixin provides shortcuts methods to manipulate and check the
    privileges granted to a role, be it a custom class or Role instance.
    """

    def role_type(self):
        """Return the role type of this instance."""
        return self.__class__.__name__

    def role_id(self):
        """Return the role ID of this instance."""
        if hasattr(self, 'id'):
            return self.id
        return None

    def is_child_of(self, role, role_id=None):
        """
        Check if this role is a child of the given role.

        It is equivalent to check if this role can inherit privileges
        from the given role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (int): only used when role is a string.

        Returns:
            bool: True or False
        """
        try:
            RoleHierarchy.objects.get(
                role_type_a=self.role_type(), role_id_a=self.role_id(),
                role_type_b=role.role_type(), role_id_b=role.role_id())
            return True
        except RoleHierarchy.DoesNotExist:
            return False

    def parents(self):
        """Return the parents of this role."""
        return RoleHierarchy.above(self.role_type(), self.role_id())

    def is_parent_of(self, role, role_id=None):
        """
        Check if this role is a parent of the given role.

        It is equivalent to check if this role can transmit its privileges
        to the given role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (int): only used when role is a string.

        Returns:
            bool: True or False
        """
        try:
            RoleHierarchy.objects.get(
                role_type_a=role.role_type(), role_id_a=role.role_id(),
                role_type_b=self.role_type(), role_id_b=self.role_id())
            return True
        except RoleHierarchy.DoesNotExist:
            return False

    def children(self):
        """Return the children of this role."""
        return RoleHierarchy.below(self.role_type(), self.role_id())

    def join(self, role, role_id=None):
        """
        Set this role as child of the given role.

        The child role will then inherit privileges from the parent role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (int): only used when role is a string.

        Returns:
            obj: the created RoleHierarchy object.
        """
        return RoleHierarchy.objects.create(
            role_type_a=self.role_type(), role_id_a=self.role_id(),
            role_type_b=role.role_type(), role_id_b=role.role_id())

    def receive(self, role, role_id=None):
        """
        Set this role as parent of the given role.

        The parent role will then transmit privileges to the child role.

        Args:
            role (str/role): a string describing the role, or a role instance.
            role_id (int): only used when role is a string.

        Returns:
            obj: the created RoleHierarchy object.
        """
        return RoleHierarchy.objects.create(
            role_type_a=self.role_type(), role_id_a=self.role_id(),
            role_type_b=role.role_type(), role_id_b=role.role_id())

    def can(self, perm, resource):
        """
        Check if this role has privilege ``perm`` on resource.

        Args:
            perm (str): string describing permission or privilege.
            resource (obj): a resource instance.

        Returns:
            bool: True or False
        """
        return RolePrivilege.authorize(
            role_type=self.role_type(), role_id=self.role_id(), perm=perm,
            resource_type=resource.resource_type(),
            resource_id=resource.resource_id())


class Role(models.Model, RoleMixin):
    """Concrete model for roles."""

    type = models.CharField(max_length=255)

    def role_type(self):
        """Override role_type method and return type attribute."""
        return self.type


class RoleHierarchy(models.Model):
    """Role hierarchy model."""

    role_type_a = models.CharField(max_length=255)
    role_id_a = models.PositiveIntegerField()
    role_type_b = models.CharField(max_length=255)
    role_id_b = models.PositiveIntegerField()

    class Meta:
        """Meta class for Django."""

        unique_together = (
            'role_type_a', 'role_id_a',
            'role_type_b', 'role_id_b'
        )

    # TODO: return Role objects and other models instances thanks to mapping?
    @staticmethod
    def above(role_type, role_id):
        """
        Return parents (roles above) of given role_type, role_id.

        Args:
            role_type (str): string describing the role type.
            role_id (int): unique ID of the role.

        Returns:
            list: list of (role_type, role_id) parents.
        """
        return [(rh.role_type_b, rh.role_id_b)
                for rh in RoleHierarchy.objects.filter(
                role_type_a=role_type, role_id_a=role_id)]

    # TODO: return Role objects and other models instances thanks to mapping?
    @staticmethod
    def below(role_type, role_id):
        """
        Return children (roles below) of given role_type, role_id.

        Args:
            role_type (str): string describing the role type.
            role_id (int): unique ID of the role.

        Returns:
            list: list of (role_type, role_id) children.
        """
        return [(rh.role_type_a, rh.role_id_a)
                for rh in RoleHierarchy.objects.filter(
                role_type_b=role_type, role_id_b=role_id)]


class RolePrivilege(models.Model):
    """Role privilege model."""

    role_type = models.CharField(_('Role type'), max_length=255)
    role_id = models.PositiveIntegerField(_('Role ID'))

    authorized = models.BooleanField(
        _('Authorization'), default=AppSettings.get_default_response())
    access_type = models.CharField(_('Access type'), max_length=255)

    resource_type = models.CharField(_('Resource type'), max_length=255)
    resource_id = models.PositiveIntegerField(_('Resource ID'), null=True)

    creation_date = models.DateTimeField(_('Created'), auto_now_add=True)
    modification_date = models.DateTimeField(_('Last modified'), auto_now=True)

    class Meta:
        """Meta class for Django."""

        unique_together = (
            'role_type', 'role_id',
            'access_type',
            'resource_type', 'resource_id'
        )

    def __str__(self):
        return '%s %s %s %s for %s %s' % (
            'allow' if self.authorized else 'deny', self.access_type,
            self.resource_type, self.resource_id if self.resource_id else '',
            self.role_type, self.role_id)

    @staticmethod
    def authorize(role_type,
                  role_id,
                  perm,
                  resource_type,
                  resource_id,
                  skip_implicit=False,
                  log=True):
        """
        Authorize access to a resource to a role.

        This method checks if a role has access to a resource or a type of
        resource. Calling this method will also try to record an entry log
        in the corresponding access attempt model.

        Call will not break if there is no access attempt model. Simply,
        nothing will be recorded.

        Args:
            role_type (str): the string describing the role.
            role_id (int): the unique ID of the role.
            perm (Permission's constant): one of the permissions available
                in Permission class.
            resource_type (str): the string describing the resource.
            resource_id (int): the unique ID of the resource.
            log (bool): record an entry in access history model or not.
            skip_implicit (bool): whether to skip implicit authorization.
                It will always be skipped if you set ACCESS_CONTROL_IMPLICIT
                setting to False.

        Returns:
            bool: role has perm on resource (or not).
        """
        attempt = AccessHistory(role_type=role_type, role_id=role_id,
                                resource_type=resource_type,
                                resource_id=resource_id, access_type=perm)
        attempt.response = None
        attempt.response_type = AccessHistory.EXPLICIT

        # Check role explicit perms
        attempt.response = RolePrivilege.authorize_explicit(
            role_type, role_id, perm, resource_type, resource_id)

        if attempt.response is None:

            # Else check inherited explicit perms
            for above_role_type, above_role_id in RoleHierarchy.above(role_type, role_id):  # noqa
                attempt.response = RolePrivilege.authorize_explicit(
                    above_role_type, above_role_id, perm,
                    resource_type, resource_id)

                if attempt.response is not None:
                    attempt.inherited_type = above_role_type
                    attempt.inherited_id = above_role_id
                    break

        # Else check role implicit perms
        if attempt.response is None and not skip_implicit:
            attempt.response = RolePrivilege.authorize_implicit(
                role_type, role_id, perm, resource_type, resource_id)

            if attempt.response is not None:
                attempt.response_type = AccessHistory.IMPLICIT

            # Else check inherited implicit perms
            else:

                for above_role_type, above_role_id in RoleHierarchy.above(role_type, role_id):  # noqa
                    attempt.response = RolePrivilege.authorize_implicit(
                        above_role_type, above_role_id, perm,
                        resource_type, resource_id)

                    if attempt.response is not None:
                        attempt.response_type = AccessHistory.IMPLICIT
                        attempt.inherited_type = above_role_type
                        attempt.inherited_id = above_role_id
                        break

        # Else give default response
        if attempt.response is None:
            attempt.response = AppSettings.get_default_response()
            attempt.response_type = AccessHistory.DEFAULT

        if log:
            attempt.save()

        return attempt.response

    @staticmethod
    def authorize_explicit(role_type,
                           role_id,
                           perm,
                           resource_type,
                           resource_id=None):
        """
        Run an explicit authorization check.

        Args:
            role_type (str): a string describing the type of role.
            role_id (int): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (int): the resource's ID.

        Returns:

        """
        try:
            rule = RolePrivilege.objects.get(
                role_type=role_type, role_id=role_id,
                resource_type=resource_type, resource_id=resource_id,
                access_type=perm)
            return rule.authorized
        except RolePrivilege.DoesNotExist:
            return None

    # TODO: implement this in some way
    @staticmethod
    def authorize_implicit(role_type,
                           role_id,
                           perm,
                           resource_type,
                           resource_id=None):
        """
        Run an implicit authorization check.

        This method checks that the given permission can be implicitly
        obtained through the ``implicit_perms`` method.

        Args:
            role_type (str): a string describing the type of role.
            role_id (int): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (int): the resource's ID.

        Returns:
            bool: denied(perm) or allowed(perm) found in implicit_perms().
            None: if ACCESS_CONTROL_IMPLICIT is False,
                or perm is in ignored_perms.
        """
        return None

    @staticmethod
    def allow(role_type,
              role_id,
              perm,
              resource_type,
              resource_id=None,
              user=None,
              log=True):
        """
        Explicitly give perm to role on resource.

        Args:
            role_type (str): a string describing the type of role.
            role_id (int): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (int): the resource's ID.
            user (User): an instance of settings.AUTH_USER_MODEL.
            log (bool): whether to record an entry in rules history.

        Returns:
            access instance: the created rule.
        """
        rule, created = RolePrivilege.objects.update_or_create(
            role_type=role_type,
            role_id=role_id,
            access_type=perm,
            resource_type=resource_type,
            resource_id=resource_id,
            defaults={'authorized': True})

        if log:
            record = PrivilegeHistory(
                user=user, action={True: PrivilegeHistory.CREATE}.get(
                    created, PrivilegeHistory.UPDATE))
            record.update_from_rule(rule)

        return rule

    @staticmethod
    def deny(role_type,
             role_id,
             perm,
             resource_type,
             resource_id=None,
             user=None,
             log=True):
        """
        Explicitly remove perm to role on resource.

        Args:
            role_type (str): a string describing the type of role.
            role_id (int): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (int): the resource's ID.
            user (User): an instance of settings.AUTH_USER_MODEL.
            log (bool): whether to record an entry in rules history.

        Returns:
            access instance: the created rule.
        """
        rule, created = RolePrivilege.objects.update_or_create(
            role_type=role_type,
            role_id=role_id,
            access_type=perm,
            resource_type=resource_type,
            resource_id=resource_id,
            defaults={'authorized': False})

        if log:
            record = PrivilegeHistory(
                user=user, action={True: PrivilegeHistory.CREATE}.get(
                    created, PrivilegeHistory.UPDATE))
            record.update_from_rule(rule)

        return rule

    @staticmethod
    def forget(role_type,
               role_id,
               perm,
               resource_type,
               resource_id=None,
               user=None,
               log=True):
        """
        Forget any rule present between role and resource.

        Args:
            role_type (str): a string describing the type of role.
            role_id (int): the role's ID.
            perm (str): one of the permissions available in Permission class.
            resource_type (str): a string describing the type of resource.
            resource_id (int): the resource's ID.
            user (User): an instance of settings.AUTH_USER_MODEL.
            log (bool): whether to record an entry in rules history.

        Returns:
            int, dict: the number of rules deleted and a dictionary with the
            number of deletions per object type (django's delete return).
        """
        try:
            rule = RolePrivilege.objects.get(
                role_type=role_type, role_id=role_id,
                resource_type=resource_type, resource_id=resource_id,
                access_type=perm)

            if log:
                PrivilegeHistory.objects.create(
                    user=user, action=PrivilegeHistory.DELETE,
                    reference_id=rule.id)

            rule.delete()
            return True
        except RolePrivilege.DoesNotExist:
            return False


# TODO: implement HierarchyHistory model?


class PrivilegeHistory(models.Model):
    """Privilege history model."""

    rule_type = 'generic'

    CREATE = 'c'
    # READ = 'r'  # makes no sense here
    UPDATE = 'u'
    DELETE = 'd'

    ACTIONS_VERBOSE = {
        CREATE: 'create',
        # READ: 'read',
        UPDATE: 'update',
        DELETE: 'delete'
    }

    ACTIONS = (
        CREATE, _(ACTIONS_VERBOSE[CREATE]),
        # READ, _(ACTIONS_VERBOSE[READ]),
        UPDATE, _(ACTIONS_VERBOSE[UPDATE]),
        DELETE, _(ACTIONS_VERBOSE[DELETE]),
    )

    reference_id = models.PositiveIntegerField(_('Rule reference ID'))
    reference = models.ForeignKey(
        RolePrivilege, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Rule reference'), related_name='history')
    action = models.CharField(_('Action'), max_length=1, choices=ACTIONS)
    datetime = models.DateTimeField(_('Date and time'), auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        verbose_name=_('User'), related_name='rules_changes',
        null=True)

    actor_type = models.CharField(_('Actor type'), max_length=255, blank=True)
    actor_id = models.PositiveIntegerField(_('Actor ID'), null=True)

    authorized = models.NullBooleanField(_('Authorization'), default=None)
    access_type = models.CharField(
        _('Access type'), max_length=255, blank=True)

    resource_type = models.CharField(
        _('Resource type'), max_length=255, blank=True)
    resource_id = models.PositiveIntegerField(_('Resource ID'), null=True)

    class Meta:
        """Meta class for Django."""

        abstract = True

    def __str__(self):
        return '[%s] user %s has %sd rule <%s>' % (
            self.datetime, self.user,
            PrivilegeHistory.ACTIONS_VERBOSE[str(self.action)],
            self.reference if self.reference else self.reference_id)

    def update_from_privilege(self, privilege, save=True):
        """
        Update this object with given privilege's attributes.

        Args:
            privilege (RolePrivilege): privilege to update from.
            save (bool): whether to commit the changes to the database.
        """
        self.reference = privilege
        self.reference_id = privilege.id
        self.actor_type = privilege.actor_type
        self.actor_id = privilege.actor_id
        self.authorized = privilege.authorized
        self.access_type = privilege.access_type
        self.resource_type = privilege.resource_type
        self.resource_id = privilege.resource_id
        if save:
            self.save()


class AccessHistory(models.Model):
    """Access history model."""

    DEFAULT = 'd'
    IMPLICIT = 'i'
    EXPLICIT = 'e'

    RESPONSE_TYPE_VERBOSE = {
        DEFAULT: 'by default',
        IMPLICIT: 'implicitly',
        EXPLICIT: 'explicitly'
    }

    RESPONSE_TYPE = (
        (DEFAULT, _(RESPONSE_TYPE_VERBOSE[DEFAULT])),
        (IMPLICIT, _(RESPONSE_TYPE_VERBOSE[IMPLICIT])),
        (EXPLICIT, _(RESPONSE_TYPE_VERBOSE[EXPLICIT]))
    )

    role_type = models.CharField(_('Actor type'), max_length=255, blank=True)
    role_id = models.PositiveIntegerField(_('Actor ID'), null=True)

    # We don't want to store false info, None says "we don't know"
    response = models.NullBooleanField(_('Response'), default=None)
    response_type = models.CharField(
        _('Response type'), max_length=1, choices=RESPONSE_TYPE)
    access_type = models.CharField(_('Access'), max_length=255)

    resource_type = models.CharField(_('Resource type'), max_length=255)
    resource_id = models.PositiveIntegerField(_('Resource ID'), null=True)

    datetime = models.DateTimeField(_('Date and time'), default=timezone.now)

    inherited_type = models.CharField(_('Group type'), max_length=255, blank=True)  # noqa
    inherited_id = models.PositiveIntegerField(_('Group ID'), null=True)

    def __str__(self):
        inherited = ''
        if self.actor_type and self.group_type and self.group_id:
            if self.actor_id:
                actor = '%s %s' % (self.actor_type, self.actor_id)
            else:
                actor = self.actor_type
            inherited = ' (inherited from %s %s)' % (
                self.group_type, self.group_id)
        elif self.group_type:
            if self.group_id:
                actor = '%s %s' % (self.group_type, self.group_id)
            else:
                actor = self.group_type
        else:
            return 'invalid: no actor & no group: %s' % self.__dict__

        authorized = 'authorized' if self.response else 'unauthorized'
        string = '[%s] %s was %s %s to %s %s %s' % (
            self.datetime, actor,
            AccessHistory.RESPONSE_TYPE_VERBOSE[str(self.response_type)],
            authorized, self.access_type, self.resource_type, self.resource_id)
        if inherited:
            return string + inherited
        return string
