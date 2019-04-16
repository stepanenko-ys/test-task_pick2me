from django.db import models


class Post(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return f'Post by user {self.user.username}'

    def add_like(self):
        """
        Adds like.
        :return: None
        """
        self.like += 1
        self.save()

    def add_dislike(self):
        """
        Adds dislike.
        :return: None
        """
        self.dislike += 1
        self.save()
