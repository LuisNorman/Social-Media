from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka  # allow ppl to write markup in their post

from groups.models import Group  # connect post to a group

# Create your models here.

from django.contrib.auth import get_user_model

User = get_user_model()  # connect current post to whoever is logged in so we can get current user logged in to session


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)  # saves the html version
        super().save(*args, **kwargs)

    def get_absolute_url(self):  # go to post/s
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']  # ("-" means sort desc
        unique_together = ['user', 'message']  # every message is uniquely linked to a user
