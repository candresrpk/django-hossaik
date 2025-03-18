from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from uuid import uuid4

# Create your models here.


class publishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT
                              )

    objects = models.Manager()
    published = publishedManager()

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(uuid4()))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} by {self.author.username}'
