from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        ordering = ('first_name', 'last_name',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_full_name()


class CollectionGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    slug = models.SlugField(unique=True, blank=True, max_length=50,
                            verbose_name='Адрес страницы с группой коллекций')
    description = models.TextField(max_length=300, blank=True,
                                   verbose_name='Описание группы')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)


class Collection(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название коллекции')
    description = models.TextField(max_length=300, blank=True,
                                   verbose_name='Описание коллекции')
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания коллекции')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True,
                              verbose_name='Фото коллекции')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                              related_name='collections',
                              verbose_name='Создатель коллекции')
    group = models.ForeignKey(CollectionGroup, on_delete=models.CASCADE,
                              related_name='collections',
                              verbose_name='Группа коллекций')

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.name


class CollectionItem(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Название объекта')
    description = models.TextField(max_length=200, blank=True,
                                   verbose_name='Описание объекта')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,
                                   related_name='collection_items',
                                   verbose_name='Коллекция объектов')
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания объекта коллекции')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Photo(models.Model):
    item = models.ForeignKey(CollectionItem, on_delete=models.CASCADE,
                             related_name='photos')
    file = models.FileField(_('Photo'), upload_to='photos/')


class Comment(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,
                                   related_name='comments',
                                   verbose_name='Название коллекции')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор коллекции')
    text = models.TextField(max_length=200, blank=False,
                            verbose_name='Текст комментария')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                       related_name='comments', default=None,
                                       null=True,
                                       verbose_name='Родительский комментарий')
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания комментария')

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='followed', verbose_name='Подписчик')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='followers',
                               verbose_name='Автор коллекции')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'user'],
                                    name='unique_following')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='favorite_collection')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,
                                   related_name='favorite_collection')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'collection'],
                                    name='unique_favorite')
        ]
