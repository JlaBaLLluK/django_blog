from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.TextField(null=False)
    publish_date = models.DateField(auto_now=True)
    author = models.ForeignKey(to=user_model, on_delete=models.CASCADE, related_name='posts', null=False)

    class Meta:
        db_table = 'Posts'
