# models.py
from django.contrib.auth.models import User
from django.db import models
from posts.models import Post 

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_bookmarks', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'), ('user', 'profile'))

    def __str__(self):
        if self.profile:
            return f"{self.user.username} bookmarked {self.profile.username}'s profile"
        elif self.post:
            return f"{self.user.username} bookmarked a post"