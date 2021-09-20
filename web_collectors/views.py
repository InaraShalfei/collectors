from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from web_collectors.forms import CollectionForm, ItemForm
from web_collectors.models import Collection, CollectionGroup, CollectionItem, User


def index(request):
    #TODO: decide what to represent on the main page
    collections = Collection.objects.order_by('-creation_date')
    paginator = Paginator(collections, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/index.html', {
        'page': page, 'paginator': paginator, 'collections': collections
    })


def collection_groups(request):
    groups = CollectionGroup.objects.all()
    paginator = Paginator(groups, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/groups.html', {'page': page, 'paginator': paginator})


def collection_group(request, slug):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collections = group.collections.all()
    paginator = Paginator(collections, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/group.html', {'page': page, 'paginator': paginator, 'group': group})


@login_required
def create_collection(request):
    form = CollectionForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST" and form.is_valid():
        collection = form.save(commit=False)
        collection.owner = request.user
        form.save()
        return redirect('web_collectors:groups')
    return render(request, 'web_collectors/new.html', {"form": form})


def update_collection(request, slug,  collection_name):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, name=collection_name)
    author = collection.owner
    if request.user != author:
        return redirect('web_collectors:groups')
    form = CollectionForm(request.POST or None,
                          files=request.FILES or None, instance=collection)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('web_collectors:group', slug=slug)
    return render(request, 'web_collectors/new.html', {
        'form': form, 'group': group, 'collection': collection, 'author': author
    })


def collection(request, slug, collection_name):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, name=collection_name)
    items = CollectionItem.objects.filter(collection=collection)
    paginator = Paginator(items, 3)
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


@login_required
def create_item(request, slug, collection_name):
    form = ItemForm(request.POST or None, files=request.FILES or None)
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, name=collection_name)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.collection = collection
        collection.owner = request.user
        form.save()
        return redirect('web_collectors:collection', slug=slug, collection_name=collection)
    return render(request, 'web_collectors/new_item.html', {"form": form, 'group': group, 'collection': collection})


def update_item(request, slug, collection_name, item_name):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, name=collection_name)
    author = collection.owner
    if request.user != author:
        return redirect('web_collectors:group')
    item = get_object_or_404(CollectionItem, collection=collection, name=item_name)
    form = ItemForm(request.POST or None,
                    files=request.FILES or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('web_collectors:item', slug=slug, collection_name=collection_name, item_name=item)
    return render(request, 'web_collectors/new_item.html', {
        'form': form, 'group': group, 'collection': collection, 'author': author, 'item': item
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    collections = Collection.objects.filter(owner=author)
    paginator = Paginator(collections, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/profile.html', {
        'page': page, 'paginator': paginator, 'collection': collection, 'author': author
    })

