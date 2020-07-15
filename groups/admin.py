from django.contrib import admin
from . import models
# Register your models here.

# adds the ability for when you click on group in
# the admin page, it will also show the group members
class GroupMemberInline(admin.TabularInline):
    models = models.GroupMember

# register models with admin
admin.site.register(models.Group)
