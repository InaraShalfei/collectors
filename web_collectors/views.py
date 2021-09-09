from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from web_collectors.models import Collection


def index(request):
    collections = Collection.objects.order_by('-creation_date')[:10]
    paginator = Paginator(collections, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'web_collectors/index.html', {'page': page, 'paginator': paginator})
