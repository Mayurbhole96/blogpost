from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True,verbose_name='Is Active')
    is_deleted = models.BooleanField(default=False,verbose_name="Is Deleted")

    class Meta:
        db_table = "table_post"
        verbose_name_plural = "Post"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "table_like"
        verbose_name_plural = "Like"