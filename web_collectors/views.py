from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import (HttpResponseRedirect, JsonResponse,
                         HttpResponseNotAllowed)

from django.shortcuts import render, get_object_or_404, redirect

from web_collectors.forms import CollectionForm, ItemForm, CommentForm
from web_collectors.models import (Collection, CollectionGroup, CollectionItem,
                                   CustomUser, Follow, Comment, Photo,
                                   Favorite)
from collectors.tasks import (delayed_collection_watermark,
                              delayed_photo_watermark,
                              delayed_send_message_collection,
                              delayed_send_message_item,
                              delayed_send_message_comment,
                              delayed_send_message_reply_comment,
                              delayed_send_message_follow)
from web_collectors.search_providers import group_search, collection_search, \
    item_search, author_search


def index(request):
    top_collections = Collection.objects.annotate(
        favorited=Count(
            'favorite_collection')).order_by('-favorited')[:4]
    paginator = Paginator(top_collections, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/index.html', {
        'page': page, 'paginator': paginator, 'collections': top_collections
    })


def all_authors(request):
    users = CustomUser.objects.order_by('id')
    paginator = Paginator(users, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/all_authors.html', {
        'page': page, 'paginator': paginator, 'users': users
    })


def collection_groups(request):
    groups = CollectionGroup.objects.all()
    paginator = Paginator(groups, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/groups.html',
                  {'page': page, 'paginator': paginator})


def collection_group(request, slug):
    form = CollectionForm(request.POST or None, files=request.FILES or None)
    group = get_object_or_404(CollectionGroup, slug=slug)
    collections = group.collections.all()
    paginator = Paginator(collections, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/group.html',
                  {'page': page, 'paginator': paginator, 'group': group,
                   'collection_form': form})


@login_required
def create_collection(request):
    form = CollectionForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        collection = form.save(commit=False)
        collection.owner = request.user
        form.save()
        delayed_collection_watermark.delay(collection.id)
        delayed_send_message_collection.delay(collection.id)
    return JsonResponse({'status': 'Success'})


@login_required
def update_collection(request, slug, collection_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    if request.user != author:
        return redirect('web_collectors:groups')
    form = CollectionForm(request.POST or None,
                          files=request.FILES or None, instance=collection)
    if request.method == 'POST' and form.is_valid():
        form.save()
        delayed_collection_watermark.delay(collection.id)
        return HttpResponseRedirect(request.POST.get('next', '/'))
    return JsonResponse({'status': 'Success'})


@login_required
def delete_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    if request.user != collection.owner:
        return redirect('web_collectors:groups')
    if request.method == 'POST':
        collection.delete()
    return JsonResponse({'status': 'Success'})


def collection(request, slug, collection_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    items = CollectionItem.objects.filter(collection=collection)
    item_form = ItemForm()
    collection_form = CollectionForm(instance=collection)
    comment_form = CommentForm()
    paginator = Paginator(items, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'web_collectors/collection.html',
                  {'page': page, 'paginator': paginator, 'group': group,
                   'collection': collection, 'author': author,
                   'comments': collection.comments.filter(parent_comment=None),
                   'collection_form': collection_form, 'comment_form': comment_form,
                   'item_form': item_form})


@login_required
def add_comment(request, collection_id):
    form = CommentForm(request.POST or None)
    collection = get_object_or_404(Collection, id=collection_id)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.collection = collection
        comment.save()
        delayed_send_message_comment(comment.id)
    return JsonResponse({'status': 'Success'})


@login_required
def reply_comment(request, collection_id, comment_id):
    collection = get_object_or_404(Collection, id=collection_id)
    comment = get_object_or_404(Comment, collection=collection, id=comment_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.author = request.user
        reply.collection = collection
        reply.parent_comment = comment
        reply.save()
        delayed_send_message_reply_comment(reply.id)
    return JsonResponse({'status': 'Success'})


@login_required
def delete_comment(request, collection_id, comment_id):
    collection = get_object_or_404(Collection, id=collection_id)
    comment = get_object_or_404(Comment, collection=collection, id=comment_id)
    if request.method == 'POST':
        comment.delete()
    return JsonResponse({'status': 'Success'})


@login_required
def update_comment(request, collection_id, comment_id):
    collection = get_object_or_404(Collection, id=collection_id)
    comment = get_object_or_404(Comment, collection=collection, id=comment_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
    return JsonResponse({'status': 'Success'})


def collection_item(request, slug, collection_id, item_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    item_form = ItemForm(instance=item)
    return render(request, 'web_collectors/item.html',
                  {'group': group, 'item': item, 'collection': collection,
                   'author': author, 'item_form': item_form})


@login_required
def create_item(request, slug, collection_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    form = ItemForm(request.POST or None, files=request.FILES or None)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not form.is_valid():
        return JsonResponse({'status': 'Invalid form', 'errors': form.errors},
                            status=422)
    item = form.save(commit=False)
    item.collection = collection
    item.save()
    for photo_data in form.cleaned_data['photos']:
        photo = Photo.objects.create(file=photo_data, item=item)
        delayed_photo_watermark.delay(photo.id)
    delayed_send_message_item(item.id)
    return JsonResponse({'status': 'Success'})


@login_required
def update_item(request, slug, collection_id, item_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    if request.user != author:
        return redirect('web_collectors:group')
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    form = ItemForm(request.POST or None,
                    files=request.FILES or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        for photo_data in form.cleaned_data['photos']:
            photo = Photo.objects.create(file=photo_data, item=item)
            delayed_photo_watermark.delay(photo.id)
        return HttpResponseRedirect(request.POST.get('next', '/'))
    return JsonResponse({'status': 'Success'})


@login_required
def delete_item(request, slug, collection_id, item_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    item.delete()
    return redirect('web_collectors:collection', slug=slug,
                    collection_id=collection_id)


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.item.collection.owner == request.user:
        photo.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile(request, username):
    form = CollectionForm(request.POST or None, files=request.FILES or None)
    author = get_object_or_404(CustomUser, username=username)
    collections = Collection.objects.filter(owner=author)
    paginator = Paginator(collections, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = request.user.is_authenticated and Follow.objects.filter(
        author=author, user=request.user).exists()
    return render(request, 'web_collectors/profile.html', {
        'page': page, 'paginator': paginator, 'collection': collection,
        'author': author,
        'following': following, 'collection_form': form})


def author_collection(request, username, collection_id):
    author = get_object_or_404(CustomUser, username=username)
    collection = get_object_or_404(Collection, owner=author, id=collection_id)
    group = collection.group
    items = CollectionItem.objects.filter(collection=collection)
    paginator = Paginator(items, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    item_form = ItemForm()
    collection_form = CollectionForm(instance=collection)
    comment_form = CommentForm()
    return render(request, 'web_collectors/author_collection.html', {
        'page': page, 'paginator': paginator, 'author': author,
        'collection': collection, 'group': group,
        'comments': collection.comments.filter(parent_comment=None),
        'collection_form': collection_form, 'comment_form': comment_form,
        'item_form': item_form})


def author_collection_item(request, username, collection_id, item_id):
    author = get_object_or_404(CustomUser, username=username)
    collection = get_object_or_404(Collection, owner=author, id=collection_id)
    group = collection.group
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    item_form = ItemForm(instance=item)
    return render(request, 'web_collectors/author_collection_item.html', {
        'author': author, 'item': item, 'collection': collection,
        'group': group, 'item_form': item_form})


@login_required
def follow_index(request):
    followed = request.user.followed.get_queryset().order_by('id')
    paginator = Paginator(followed, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/follow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(CustomUser, username=username)
    if request.user != author:
        follow, created = Follow.objects.get_or_create(author=author,
                                                       user=request.user)
        delayed_send_message_follow(follow.id)
    return JsonResponse({'status': 'Success'})


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        get_object_or_404(Follow, user=request.user, author=author).delete()
    return JsonResponse({'status': 'Success'})


@login_required
def favorite_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    user = request.user
    if user != collection.owner:
        Favorite.objects.get_or_create(collection=collection, user=user)
    return JsonResponse({'status': 'Success'})


@login_required
def search(request):
    el = request.GET.get('q')
    providers = [group_search, collection_search, item_search, author_search]
    lst = [provider(el) for provider in providers]
    results = list(filter(None, list(OrderedDict.fromkeys(lst))))
    # paginator = Paginator(results, 1)
    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)

    return render(request, 'includes/search.html', {'results': results})
                                                    # 'page': page,
                                                    # 'paginator': paginator})


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'misc/403.html', status=403)
