from django.db import models
from django.utils.text import slugify # removes chars that aren't alha numerics, underscoeres, hypens. Needed for urls - replace spaces with hypens
from django.conf import settings
from django.urls import reverse

import misaka # link embedding. put links or mark down text

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library() # custom template tags. allow In group tags


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember') # all the members that belong to this group

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) # slugify the name of group = making the name into a valid url name (i.e. no space or alpha numerics)
        self.description_html = misaka.html(self.description) # incase there is markdown in the description, misake will be able to handle it
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

# Group member connects to a group that it belongs to
# and a user that connects to the actual group member
class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships", on_delete=models.CASCADE) # this group member is related to the foreign key 'memberships'
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    # return str representation of user's username
    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
