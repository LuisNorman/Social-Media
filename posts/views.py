from django.contrib import messages
from django.shortcuts import render
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin  # someone needs to be actually logged in to perform post actions (i.e. create post)
from django.urls import reverse_lazy  # in case someone wants to delete a post (go back to previous page)

from django.http import Http404  # add the ability to return a 404 page
from django.views import generic  # generic class based views

from braces.views import SelectRelatedMixin  #
from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()  # User = get current user. So we can play with User object in all the classes if needed

# when you see a user or group, you can see their posts
## shows the posts that are related to a user or a group or bot
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')   # the user and the group the post belongs to

# List view for a user's specific post
class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    # check if user actually exists then show their post
    def get_queryset(self):  # try
        try:
            # set the post of this user of this particular post to the user that this post belongs to (self.post_user is an attribuutte we create)
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    #  return the context data of the user of this particular post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user  # grab the post user and add a field for it in the conext dict
        return context

# when you select a post, it shows the details
class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')  # the user and group that this post detail belongs to

    def get_queryset(self):
        queryset = super().get_queryset()  # get the queryset of this actual post
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))  # filter where the username is equal to username of the object that calls this


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):

    fields = ('message', 'group')  # the fields that are editable
    model = models.Post


    def form_valid(self, form):
        self.object = form.save(commit=False)  # set object to be form
        self.object.user = self.request.user  # set user of form object to be of user who sent request
        self.object.save()  # save object
        return super().form_valid(form)
    
class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')  # once the delete is confirmed, it gets sent to post:all

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)

