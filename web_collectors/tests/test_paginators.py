import datetime
from collections import namedtuple

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now

from web_collectors.models import CollectionGroup, User, Collection, CollectionItem, Follow


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serialized_rollback = True
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

    def test_pages_with_ten_records_have_correct_context(self):
        Address = namedtuple('Address', 'address text1 text2')
        addresses = [((reverse('web_collectors:index')), 'Russian poems', 'Russian authors3'),
                     ((reverse('web_collectors:groups')), 'Книги0', 'Книги7'),
                    ]
        for address, text1, text2 in addresses:
            with self.subTest(address=address):
                new_address = Address(address, text1, text2)
                response = self.guest_client.get(new_address.address)
                page_collections = response.context['page']
                first_record = page_collections[0]
                first_record_name = first_record.name
                last_record = page_collections[9]
                last_record_name = last_record.name
                self.assertEqual(first_record_name, new_address.text1)
                self.assertEqual(last_record_name, new_address.text2)

    def test_pages_with_three_records_have_correct_context(self):
        Url = namedtuple('Url', 'address text1 text2')
        urls = [((reverse('web_collectors:group', kwargs={'slug': 'poems'})), 'Russian poems', 'Russian authors10'),
                ((reverse('web_collectors:collection', kwargs={'slug': 'poems', 'collection_id': 13})),
                 'Pushkin poems0', 'Pushkin poems2'),
                ((reverse('web_collectors:author_collection', kwargs={'username': 'Ira', 'collection_id': 13})),
                 'Pushkin poems0', 'Pushkin poems2')]
        for address, text1, text2 in urls:
            with self.subTest(address=address):
                new_url = Url(address, text1, text2)
                response = self.authorized_client.get(new_url.address)
                page_collections = response.context['page']
                first_record = page_collections[0]
                first_record_name = first_record.name
                last_record = page_collections[2]
                last_record_name = last_record.name
                self.assertEqual(first_record_name, new_url.text1)
                self.assertEqual(last_record_name, new_url.text2)

    def test_all_groups_page_has_correct_context(self):
        UrlAddress = namedtuple('Url', 'address text1 text2')
        new_url_address = UrlAddress((reverse('web_collectors:all_authors')), 'Visitor', 'Boba - 3')
        address, text1, text2 = new_url_address
        response = self.guest_client.get(address)
        page_collections = response.context['page']
        first_record = page_collections[0]
        first_record_username = first_record.username
        last_record = page_collections[9]
        last_record_username = last_record.username
        self.assertEqual(first_record_username, text1)
        self.assertEqual(last_record_username, text2)

    def test_profile_page_has_correct_context(self):
        PageAddress = namedtuple('PageAddress', 'address text1 text2')
        page_address = PageAddress((reverse('web_collectors:profile', kwargs={'username': 'Ira'})), 'Russian poems',
                                   'Russian authors8')
        address, text1, text2 = page_address
        response = self.guest_client.get(address)
        page_collections = response.context['page']
        first_record = page_collections[0]
        first_record_name = first_record.name
        last_record = page_collections[4]
        last_record_name = last_record.name
        self.assertEqual(first_record_name, text1)
        self.assertEqual(last_record_name, text2)

    def test_follow_page_has_correct_context(self):
        FullAddress = namedtuple('FullAddress', 'address text1 text2')
        full_address = FullAddress((reverse('web_collectors:follow_index')), 'Borya0', 'Borya2')
        address, text1, text2 = full_address
        response = self.authorized_client.get(address)
        page_users = response.context['page']
        first_record = page_users[0]
        first_record_author = first_record.author
        last_record = page_users[2]
        last_record_author = last_record.author
        self.assertEqual(first_record_author.username, text1)
        self.assertEqual(last_record_author.username, text2)
