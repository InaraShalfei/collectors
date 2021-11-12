import datetime

from django.test import TestCase, Client
from django.urls import reverse

from web_collectors.models import CollectionGroup, User, Collection, CollectionItem


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Visitor')
        for i in range(12):
            CollectionGroup.objects.create(
                name=f'Книги{i}',
                slug=f'knigi{i}',
                description=f'All books in the world - {i}'
            )
        for i in range(12):
            User.objects.create_user(username=f'Boba - {i}')

        group = CollectionGroup.objects.create(name='Стихи', slug='poems', description='Poems of all russian authors')
        author = User.objects.create(username='Ira')
        for i in range(12):
            collection = Collection(
                name=f'Russian authors{i}',
                description=f'All books of russian authors - {i}',
                owner=author,
                group=group)
            collection.creation_date = datetime.datetime.now() - datetime.timedelta(minutes=15 - i)
            collection.save()
        collection = Collection.objects.create(name='Russian poems', description='All Russian poems',
                                               owner=author,
                                               group=group)
        for i in range(4):
            collection_item = CollectionItem(
                name=f'Pushkin poems{i}',
                description=f'Poems of A.S.Pushkin - {i}',
                collection=collection,
                position=i)
            collection_item.creation_date = datetime.datetime.now() - datetime.timedelta(minutes=15 - i)
            collection_item.save()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage_first_page_has_10_records(self):
        response = self.guest_client.get(reverse('web_collectors:index'))
        self.assertEqual(len(response.context['page']), 10)

    def test_homepage_second_page_has_2_records(self):
        response = self.guest_client.get(reverse('web_collectors:index') + '?page=2')
        self.assertEqual(len(response.context['page']), 3)
