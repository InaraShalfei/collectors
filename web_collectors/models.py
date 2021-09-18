from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from sorl.thumbnail import get_thumbnail

User = get_user_model()


class CollectionGroup(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=300, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    creation_date = models.DateTimeField(auto_created=False, default=timezone.now)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    group = models.ForeignKey(CollectionGroup, on_delete=models.CASCADE, related_name='collections')

    class Meta:
        order_with_respect_to = 'group'

    def __str__(self):
        return self.name


class Photo(models.Model):
    photo = models.ImageField(upload_to='media/photo/', blank=True, null=True)
    #item = models.ForeignKey(CollectionItem, on_delete=models.CASCADE, related_name='photos')
    position = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo = get_thumbnail(self.image, '500x600', quality=99, format='JPEG')
        super(Photo, self).save(*args, **kwargs)


class CollectionItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='collection_items')
    creation_date = models.DateTimeField(auto_created=False, default=timezone.now)
    position = models.AutoField(primary_key=True)
    photo = models.ManyToManyField(Photo)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
