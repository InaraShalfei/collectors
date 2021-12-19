from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect

from web_collectors.forms import CollectionForm, ItemForm, CommentForm
from web_collectors.models import Collection, CollectionGroup, CollectionItem, User, Follow, Comment, Photo


def index(request):
    #TODO: decide what to represent on the main page
    collections = Collection.objects.all()
    paginator = Paginator(collections, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/index.html', {
        'page': page, 'paginator': paginator, 'collections': collections
    })


def all_authors(request):
    users = User.objects.order_by('id')
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
    if request.method == 'POST' and form.is_valid():
        collection = form.save(commit=False)
        collection.owner = request.user
        form.save()
        group = collection.group
        return redirect('web_collectors:collection', slug=group.slug, collection_id=collection.id)
    return render(request, 'web_collectors/new.html', {'form': form})


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
        return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)
    return render(request, 'web_collectors/new.html', {
        'form': form, 'group': group, 'collection': collection, 'author': author})


@login_required
def delete_collection(request, slug,  collection_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    if request.user != author:
        return redirect('web_collectors:groups')
    if request.method == 'POST':
        collection.delete()
        return redirect('web_collectors:collection', slug=slug)


def collection(request, slug, collection_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    items = CollectionItem.objects.filter(collection=collection)
    paginator = Paginator(items, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    form = CommentForm()
    return render(request, 'web_collectors/collection.html', {
        'page': page, 'paginator': paginator, 'group': group, 'collection': collection, 'author': author, 'form': form,
        'comments': collection.comments.filter(parent_comment=None)
    })


@login_required
def add_comment(request, slug, collection_id):
    form = CommentForm(request.POST or None)
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.collection = collection
        comment.save()
    return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)


@login_required
def reply_comment(request, slug, collection_id, comment_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    comment = get_object_or_404(Comment, collection=collection, id=comment_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.author = request.user
        reply.collection = collection
        reply.parent_comment = comment
        reply.save()
        return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)
    return render(request, 'includes/reply_comment.html', {
        'form': form, 'group': group, 'collection': collection, 'comment': comment})


@login_required
def delete_comment(request, slug, collection_id, comment_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    comment = get_object_or_404(Comment, collection=collection, id=comment_id)
    author = comment.author
    if request.method == 'POST':
        comment.delete()
        return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)
    return render(request, 'includes/delete_comment.html', {'group': group, 'collection': collection, 'author': author,
                                                            'comment': comment})


@login_required
def update_comment(request, slug, collection_id, comment_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    comment = get_object_or_404(Comment, collection=collection, id=comment_id)
    author = comment.author
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)
    return render(request, 'includes/update_comment.html', {
        'form': form, 'group': group, 'collection': collection, 'author': author, 'comment': comment})


def collection_item(request, slug, collection_id, item_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    author = collection.owner
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    return render(request, 'web_collectors/item.html', {'group': group, 'item': item, 'collection': collection,
                                                        'author': author})


@login_required
def create_item(request, slug, collection_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    form = ItemForm(request.POST or None, files=request.FILES or None)
    author = collection.owner
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.collection = collection
        item.save()
        for photo in form.cleaned_data['photos']:
            Photo.objects.create(file=photo, item=item)
        return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)
    return render(request, 'web_collectors/new_item.html', {'form': form, 'group': group, 'collection': collection,
                                                            'author': author})


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
        for photo in form.cleaned_data['photos']:
            Photo.objects.create(file=photo, item=item)
        return redirect('web_collectors:item', slug=slug, collection_id=collection_id, item_id=item_id)
    return render(request, 'web_collectors/new_item.html', {
        'form': form, 'group': group, 'collection': collection, 'author': author, 'item': item
    })


@login_required
def delete_item(request, slug, collection_id, item_id):
    group = get_object_or_404(CollectionGroup, slug=slug)
    collection = get_object_or_404(Collection, group=group, id=collection_id)
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('web_collectors:collection', slug=slug, collection_id=collection_id)


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if photo.item.collection.owner == request.user:
        photo.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile(request, username):
    author = get_object_or_404(User, username=username)
    collections = Collection.objects.filter(owner=author)
    paginator = Paginator(collections, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = request.user.is_authenticated and Follow.objects.filter(author=author, user=request.user).exists()
    return render(request, 'web_collectors/profile.html', {
        'page': page, 'paginator': paginator, 'collection': collection, 'author': author,
        'following': following
    })


def author_collection(request, username, collection_id):
    author = get_object_or_404(User, username=username)
    collection = get_object_or_404(Collection, owner=author, id=collection_id)
    items = CollectionItem.objects.filter(collection=collection)
    paginator = Paginator(items, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    form = CommentForm()
    return render(request, 'web_collectors/author_collection.html', {
        'page': page, 'paginator': paginator, 'author': author, 'collection': collection, 'form': form,
        'comments': collection.comments.all()})


def author_collection_item(request, username, collection_id, item_id):
    author = get_object_or_404(User, username=username)
    collection = get_object_or_404(Collection, owner=author, id=collection_id)
    item = get_object_or_404(CollectionItem, collection=collection, id=item_id)
    return render(request, 'web_collectors/author_collection_item.html', {
        'user': author, 'item': item, 'collection': collection}
                  )


@login_required
def follow_index(request):
    followed = request.user.followed.get_queryset().order_by('id')
    paginator = Paginator(followed, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/follow.html', {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect('web_collectors:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if request.method == 'POST':
        get_object_or_404(Follow, user=request.user, author=author).delete()
        return redirect('web_collectors:profile', username=username)
    return render(request, 'includes/unfollow.html', {'author': author, 'user': request.user})


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'misc/403.html', status=403)
