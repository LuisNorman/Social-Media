from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse
from django.views import generic

from groups.models import Group, GroupMember

from django.shortcuts import get_object_or_404

from . import models


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')  # When someone creates a group, they can edit the name and description of the group
    model = Group


# Details of specific group
class SingleGroup(generic.DetailView):
    model = Group


# List of all available groups
class ListGroups(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    # after joining group, redirect to that group's detail page
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    # get the group user wants to join
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,
                                       group=group)  # create a group member of this user. Will fail if user is already a member
        except IntegrityError:
            messages.warning(self.request, 'Warning - You are already a member!')
        else:
            messages.success(self.request, 'You are now a member!')

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    # after leaving group, redirect to that group's detail page
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        # Retrieve the membership of the group member requesting to leave group
        try:
            print("here1")
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            print("here")
            messages.warning(self.request, 'Sorry, you are not in this group.')

        else:
            print("here3")
            membership.delete()
            messages.success(self.request, 'You have left the group!')

        return super().get(request, *args, **kwargs)
