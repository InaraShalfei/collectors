import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now

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
            collection = Collection.objects.create(
                name=f'Russian authors{i}',
                description=f'All books of russian authors - {i}',
                owner=author,
                group=group)
            collection.creation_date = now() - datetime.timedelta(minutes=15 - i)
            collection.save()
        collection = Collection.objects.create(name='Russian poems', description='All Russian poems',
                                               owner=author,
                                               group=group)
        for i in range(4):
            collection_item = CollectionItem.objects.create(
                name=f'Pushkin poems{i}',
                description=f'Poems of A.S.Pushkin - {i}',
                collection=collection,
                position=i)
            collection_item.creation_date = now() - datetime.timedelta(minutes=15 - i)
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

    def test_homepage_has_correct_context(self):
        response = self.guest_client.get(reverse('web_collectors:index'))
        page_collections = response.context['page']
        first_record = page_collections[0]
        first_record_name = first_record.name
        last_record = page_collections[9]
        last_record_name = last_record.name
        self.assertEqual(first_record_name, 'Russian poems')
        self.assertEqual(last_record_name, 'Russian authors3')




