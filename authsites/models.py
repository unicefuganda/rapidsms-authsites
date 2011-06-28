from django.db import models

from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.conf import settings

from rapidsms.models import Contact, Connection
from rapidsms_httprouter.models import Message, ForUpdateManager
from rapidsms_httprouter.managers import BulkInsertManager

from django.db.models.signals import post_save

class GroupSite(models.Model):
    group = models.ForeignKey(Group, related_name='groupsites')
    site = models.ForeignKey(Site, related_name='sitegroups')

class UserSite(models.Model):
    user = models.ForeignKey(User, related_name='usersites')
    site = models.ForeignKey(Site, related_name='siteusers')

class ContactSite(models.Model):
    contact = models.ForeignKey(Contact, related_name='contactsites')
    site = models.ForeignKey(Site, related_name='sitecontacts')
    objects = models.Manager()
    bulk = BulkInsertManager()

    @classmethod
    def add_all(cls, contacts):
        for c in contacts:
            ContactSite.bulk.bulk_insert(send_pre_save=False,
                                         contact=c,
                                         site=Site.objects.get_current())
        ContactSite.bulk.bulk_insert_commit(send_post_save=False,autoclobber=True)

class MessageSite(models.Model):
    message = models.ForeignKey(Message, related_name='messagesites')
    site = models.ForeignKey(Site, related_name='sitemessages')
    objects = models.Manager()
    bulk = BulkInsertManager()
    
    @classmethod
    def add_all(cls, messages):
        for m in messages:
            MessageSite.bulk.bulk_insert(send_pre_save=False,
                                         message=m,
                                         site=Site.objects.get_current())
        MessageSite.bulk.bulk_insert_commit(send_post_save=False,autoclobber=True)

#class ConnectionSite(models.Model):
#    connection = models.ForeignKey(Connection, related_name='connectionsites')
#    site = models.ForeignKey(Site, related_name='siteconnections')
#
#class MessageSite(models.Model):
#    message = models.ForeignKey(Message, related_name='messagesites')
#    site = models.ForeignKey(Site, related_name='sitemessages')

class GroupSiteManager(models.Manager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(GroupSiteManager, self).get_query_set().filter(pk__in=Site.objects.get_current().sitegroups.all().values_list('group__pk', flat=True))
        else:
            return super(GroupSiteManager, self).get_query_set()

class UserSiteManager(UserManager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(UserSiteManager, self).get_query_set().filter(pk__in=Site.objects.get_current().siteusers.all().values_list('user__pk', flat=True))
        else:
            return super(UserSiteManager, self).get_query_set()

class ContactSiteManager(models.Manager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(ContactSiteManager, self).get_query_set().filter(pk__in=Site.objects.get_current().sitecontacts.all().values_list('contact__pk', flat=True))
        else:
            return super(ContactSiteManager, self).get_query_set()

#class ConnectionSiteManager(models.Manager):
#    def get_query_set(self):
#        if settings.SITE_ID:
#            return super(ConnectionSiteManager, self).get_query_set().filter(pk__in=Site.objects.get_current().siteconnections.all())
#        else:
#            return super(ConnectionSiteManager, self).get_query_set()
#
class MessageSiteManager(ForUpdateManager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(MessageSiteManager, self).get_query_set().filter(pk__in=Site.objects.get_current().sitemessages.all().values_list('message__pk', flat=True))
        else:
            return super(MessageSiteManager, self).get_query_set()

gs_mgr = GroupSiteManager()
gs_mgr.contribute_to_class(Group, 'objects')
models.Manager().contribute_to_class(Group, 'allsites')

us_mgr = UserSiteManager()
us_mgr.contribute_to_class(User, 'objects')
models.Manager().contribute_to_class(User, 'allsites')

c_mgr = ContactSiteManager()
c_mgr.contribute_to_class(Contact, 'objects')
models.Manager().contribute_to_class(Contact, 'allsites')

#c_mgr = ConnectionSiteManager()
#c_mgr.contribute_to_class(Connection, 'objects')
#
c_mgr = MessageSiteManager()
c_mgr.contribute_to_class(Message, 'objects')
models.Manager().contribute_to_class(Message, 'allsites')

def sites_postsave_handler(sender, **kwargs):
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        if (sender == Contact and kwargs['created']):
            ContactSite.objects.create(contact = kwargs['instance'], site=Site.objects.get_current())
        elif (sender == User and kwargs['created']):
            UserSite.objects.create(user = kwargs['instance'], site=Site.objects.get_current())
        elif (sender == Group and kwargs['created']):
            GroupSite.objects.create(group = kwargs['instance'], site=Site.objects.get_current())
#        elif (sender == Connection and kwargs['created']):
#            ConnectionSite.objects.create(connection = kwargs['instance'], site=Site.objects.get_current())
        elif (sender == Message and kwargs['created']):
            MessageSite.objects.create(message = kwargs['instance'], site=Site.objects.get_current())
#

post_save.connect(sites_postsave_handler, weak=True)
