from django.db import models

from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.conf import settings

from rapidsms.models import Contact

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
    
class GroupSiteManager(models.Manager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(GroupSiteManager, self).get_query_set().filter(pk__in=GroupSite.objects.filter(site__pk=settings.SITE_ID).values_list('group__pk', flat=True))
        else:
            return super(GroupSiteManager, self).get_query_set()

class UserSiteManager(UserManager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(UserSiteManager, self).get_query_set().filter(pk__in=UserSite.objects.filter(site__pk=settings.SITE_ID).values_list('user__pk', flat=True))
        else:
            return super(UserSiteManager, self).get_query_set()

class ContactSiteManager(models.Manager):
    def get_query_set(self):
        if settings.SITE_ID:
            return super(ContactSiteManager, self).get_query_set().filter(pk__in=ContactSite.objects.filter(site__pk=settings.SITE_ID).values_list('contact__pk', flat=True))
        else:
            return super(ContactSiteManager, self).get_query_set()

gs_mgr = GroupSiteManager()
gs_mgr.contribute_to_class(Group, 'objects')

us_mgr = UserSiteManager()
us_mgr.contribute_to_class(User, 'objects')

c_mgr = ContactSiteManager()
c_mgr.contribute_to_class(Contact, 'objects')

def sites_postsave_handler(sender, **kwargs):
    if settings.SITE_ID:
        site = Site.objects.get_current()
        if (sender == Contact):
            ContactSite.objects.create(contact = kwargs['instance'], site=site)
        elif (sender == User):
            UserSite.objects.create(user = kwargs['instance'], site=site)
        elif (sender == Group):
            GroupSite.objects.create(group = kwargs['instance'], site=site)

post_save.connect(sites_postsave_handler, weak=True)