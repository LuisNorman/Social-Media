from django.urls import path
from . import views

app_name='posts'  # so we can use it in the template tages

urlpatterns = [
    path('', views.PostList.as_view(), name="all"),
    path("new/", views.CreatePost.as_view(), name="create"),  # in base.html where the navbar is, it calls url 'posts:create' which invokes this
    path("by/<username>/",views.UserPosts.as_view(),name="for_user"),  # i.e. go to "by/luitron/" shows all luitron's post
    path("by/<username>/<int:pk>/",views.PostDetail.as_view(),name="single"),
    path("delete/<int:pk>/",views.DeletePost.as_view(),name="delete"),
]
