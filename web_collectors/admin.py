from django.contrib import admin

from .models import Collection, CollectionItem, Photo


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_date', 'collection_owner', 'photo')
    list_filter = ('name', 'collection_owner', )
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class PhotoAdminInLine(admin.TabularInline):
    model = Photo
    extra = 1


class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'collection', 'creation_date')
    list_filter = ('name', 'collection', )
    search_fields = ('name', 'collection', )
    inlines = (PhotoAdminInLine, )
    empty_value_display = '-пусто-'


admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionItem, CollectionItemAdmin)
