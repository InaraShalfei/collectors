from django.db.models import Q

from web_collectors.models import (CollectionGroup, Collection, CollectionItem,
                                   CustomUser)


def group_search(el):
    return CollectionGroup.objects.filter(
            Q(name__icontains=el) | Q(description__icontains=el)
        )


def collection_search(el):
    return Collection.objects.filter(
            Q(name__icontains=el) | Q(description__icontains=el)
        )


def item_search(el):
    return CollectionItem.objects.filter(
            Q(name__icontains=el) | Q(description__icontains=el)
        )


def author_search(el):
    return CustomUser.objects.filter(username__icontains=el)
