from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    published = models.DateField('date published')
    content = models.TextField(blank=True)

    def __str__(self):
        return '[{}] {}'.format(self.published, self.title)

    def summary(self):
        return self.content[:100]
