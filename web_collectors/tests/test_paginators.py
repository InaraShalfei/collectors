import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now

from web_collectors.models import CollectionGroup, User, Collection, CollectionItem, Follow


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Visitor')
        for i in range(5):
            Follow.objects.create(
                user=cls.user,
                author=User.objects.create(username=f'Borya{i}')
            )
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

    def test_first_page_has_10_records(self):
        addresses = ['web_collectors:index', 'web_collectors:all_authors', 'web_collectors:groups']
        for address in addresses:
            with self.subTest(address=address):
                response = self.guest_client.get(reverse(address))
                self.assertEqual(len(response.context['page']), 10)

    def test_second_page_has_3_records(self):
        addresses = ['web_collectors:index', 'web_collectors:groups']
        for address in addresses:
            with self.subTest(address=address):
                response = self.guest_client.get(reverse(address) + '?page=2')
                self.assertEqual(len(response.context['page']), 3)

    def test_all_authors_second_page_has_9_records(self):
        response = self.guest_client.get(reverse('web_collectors:all_authors') + '?page=2')
        self.assertEqual(len(response.context['page']), 9)

    def test_first_page_has_3_records(self):
        addresses = [(reverse('web_collectors:group', kwargs={'slug': 'poems'})),
                     (reverse('web_collectors:collection', kwargs={'slug': 'poems', 'collection_id': 13})),
                     (reverse('web_collectors:author_collection', kwargs={'username': 'Ira', 'collection_id': 13})),
                     reverse('web_collectors:follow_index')]
        for address in addresses:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(len(response.context['page']), 3)

    def test_profile_first_page_has_5_records(self):
        response = self.guest_client.get(reverse('web_collectors:profile', kwargs={'username': 'Ira'}))
        self.assertEqual(len(response.context['page']), 5)

    def test_follow_last_page_has_2_records(self):
        response = self.authorized_client.get(reverse('web_collectors:follow_index') + '?page=2')
        self.assertEqual(len(response.context['page']), 2)

    def test_last_page_has_1_record(self):
        addresses = [(reverse('web_collectors:collection', kwargs={'slug': 'poems', 'collection_id': 13})),
                     (reverse('web_collectors:author_collection', kwargs={'username': 'Ira', 'collection_id': 13}))]
        for address in addresses:
            with self.subTest(address=address):
                response = self.authorized_client.get(address + '?page=2')
                self.assertEqual(len(response.context['page']), 1)

    def test_group_last_page_has_1_record(self):
        response = self.authorized_client.get(reverse('web_collectors:group', kwargs={'slug': 'poems'}) + '?page=5')
        self.assertEqual(len(response.context['page']), 1)

    def test_profile_last_page_has_1_record(self):
        response = self.authorized_client.get(reverse('web_collectors:author_collection',
                                                      kwargs={'username': 'Ira', 'collection_id': 13}) + '?page=3')
        self.assertEqual(len(response.context['page']), 1)


    def test_homepage_has_correct_context(self):
        response = self.guest_client.get(reverse('web_collectors:index'))
        page_collections = response.context['page']
        first_record = page_collections[0]
        first_record_name = first_record.name
        last_record = page_collections[9]
        last_record_name = last_record.name
        self.assertEqual(first_record_name, 'Russian poems')
        self.assertEqual(last_record_name, 'Russian authors3')
