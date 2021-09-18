from django.contrib import admin

from .models import Collection, CollectionItem, CollectionGroup, Photo


class CollectionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    list_filter = ('name', )


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_date', 'owner', 'photo', 'group')
    list_filter = ('name', 'owner', )
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'collection', 'creation_date', )
    list_filter = ('name', 'collection', )
    search_fields = ('name', 'collection', )
    empty_value_display = '-пусто-'


admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionItem, CollectionItemAdmin)
admin.site.register(CollectionGroup, CollectionGroupAdmin)
admin.site.register(Photo)
