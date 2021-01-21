from django.db import models


class Post(models.Model):
    """ Модель поста """

    title = models.CharField(max_length=200)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title
