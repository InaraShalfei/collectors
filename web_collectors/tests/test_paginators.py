from django.test import TestCase, Client

from web_collectors.models import CollectionGroup, User, Collection, CollectionItem


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(12):
            cls.group = CollectionGroup.objects.create(
                name=f'Книги{1}',
                slug=f'knigi{1}',
                description=f'All books in the world - {i}'
            )
        for i in range(12):
            cls.user = User.objects.create_user(username=f'Boba - {i}')
        for i in range(12):
            cls.collection = Collection.objects.create(
                name=f'Russian authors{i}',
                description=f'All books of russian authors - {i}',
                owner=User.objects.create(username='Ira'),
                group=CollectionGroup.objects.create(
                    name='Пластинки',
                    slug='discs',
                    description='Discs from all over the world'
                ))
        for i in range(4):
            cls.collection_item = CollectionItem.objects.create(
                name=f'Pushkin poems{i}',
                description=f'Poems of A.S.Pushkin - {i}',
                collection=Collection.objects.create(
                    name='Russian poems',
                    description='All Russian poems',
                    owner=User.objects.create(username='Ira'),
                    group=CollectionGroup.objects.create(
                        name='Стихи',
                        slug='poems',
                        description='Poems of all russian authors'
                    ),
                    position={i}))

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
