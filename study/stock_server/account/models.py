from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    birthday = models.IntegerField(default=19000101)

    def __str__(self):
        return '[{0}] {1}'.format(self.user.username, self.name)

    def create(self, user, name, birthday):
        self.user = user
        self.name = name
        self. birthday = birthday
        user.save()
        self.save()
