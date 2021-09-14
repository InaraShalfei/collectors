from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from web_collectors.models import Collection, CollectionGroup, CollectionItem


def index(request):
    collections = Collection.objects.order_by('-creation_date')
    paginator = Paginator(collections, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/index.html', {'page': page, 'paginator': paginator})


def collection_group(request, slug):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collections = group.collections.all()
    paginator = Paginator(collections, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/group.html', {'page': page, 'paginator': paginator, 'group': group})


def collection_groups(request):
    groups = CollectionGroup.objects.all()
    paginator = Paginator(groups, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/groups.html', {'page': page, 'paginator': paginator})


def collection(request, slug, collection_name):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, name=collection_name)
    items = CollectionItem.objects.filter(collection=collection)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/collection.html', {
        'page': page, 'paginator': paginator, 'group': group, 'collection': collection
    })


def collection_item(request, slug, collection_name, item_name):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, name=collection_name)
    item = get_object_or_404(CollectionItem, collection=collection, name=item_name)
    return render(request, 'web_collectors/item.html', {'group': group, 'item': item, 'collection': collection})
