from django.test import TestCase, Client
from django.urls import reverse

from web_collectors.models import (Comment, Collection, CustomUser,
                                   CollectionGroup, CollectionItem, Follow)


class CollectionUrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = CollectionGroup.objects.create(
            name='Книги',
            slug='knigi',
            description='All books in the world'
        )
        cls.group2 = CollectionGroup.objects.create(
            name='Игрушки',
            slug='toys',
            description='Все игрушки мира'
        )
        cls.user = CustomUser.objects.create_user(username='Boba',
                                                  email='boba@gmail.com')
        cls.user2 = CustomUser.objects.create_user(username='Vera',
                                                   email='vera@gmail.com')
        cls.collection = Collection.objects.create(
            name='Russian authors',
            description='All books of russian authors',
            owner=cls.user,
            group=cls.group
        )
        cls.collection2 = Collection.objects.create(
            name='Russian toys',
            description='All toys of russian authors',
            owner=cls.user2,
            group=cls.group2
        )
        cls.comment = Comment.objects.create(
            collection=cls.collection,
            author=cls.user2,
            text='Cool!',
        )
        cls.collection_item = CollectionItem.objects.create(
            name='Pushkin poems',
            description='Poems of A.S.Pushkin',
            collection=cls.collection,
        )
        cls.collection_item2 = CollectionItem.objects.create(
            name='Demchenko toys',
            description='Toys of Demchenko artist',
            collection=cls.collection2,
        )

        cls.follow = Follow.objects.create(
            user=cls.user2,
            author=cls.user
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_exist_at_desired_location_for_guest_client(self):
        url_names = [reverse('web_collectors:index'),
                     reverse('static_pages:about'),
                     reverse('users:signup')]

        for address in url_names:
            with self.subTest(adress=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200)

    def test_pages_for_guest_client_have_correct_templates(self):
        templates_url_names = {
            'web_collectors/index.html': reverse('web_collectors:index'),
            'static_pages/about.html': reverse('static_pages:about'),
            'users/signup.html': reverse('users:signup')
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_exist_at_desired_location_for_authorized_client(self):
        url_names = [reverse('web_collectors:index'),
                     reverse('static_pages:about'),
                     reverse('web_collectors:groups'),
                     reverse('web_collectors:all_authors'),
                     reverse('web_collectors:new_collection'),
                     reverse('web_collectors:follow_index'),
                     reverse('web_collectors:profile',
                             kwargs={'username': self.user2.username}),
                     reverse('web_collectors:favorite_collection',
                             kwargs={'collection_id': self.collection2.id}),
                     reverse('web_collectors:profile_follow',
                             kwargs={'username': self.user2.username}),
                     reverse('web_collectors:profile_unfollow',
                             kwargs={'username': self.user.username}),
                     reverse('web_collectors:author_collection',
                             kwargs={'username': self.user2.username,
                                     'collection_id': self.collection2.id}),
                     reverse('web_collectors:author_collection_item',
                             kwargs={'username': self.user2.username,
                                     'collection_id': self.collection2.id,
                                     'item_id': self.collection_item2.id}),
                     reverse('web_collectors:group',
                             kwargs={'slug': self.group2.slug}),
                     reverse('web_collectors:collection',
                             kwargs={'slug': self.group2.slug,
                                     'collection_id': self.collection2.id}),
                     reverse('web_collectors:update_collection',
                             kwargs={'slug': self.group.slug,
                                     'collection_id': self.collection.id}),
                     reverse('web_collectors:delete_collection',
                             kwargs={'collection_id': self.collection.id}),
                     # reverse('web_collectors:new_item',
                     #         kwargs={'slug': self.group.slug,
                     #                 'collection_id': self.collection.id}),
                     reverse('web_collectors:item',
                             kwargs={'slug': self.group.slug,
                                     'collection_id': self.collection.id,
                                     'item_id': self.collection_item.id}),
                     reverse('web_collectors:update_item',
                             kwargs={'slug': self.group.slug,
                                     'collection_id': self.collection.id,
                                     'item_id': self.collection_item.id}),
                     reverse('web_collectors:add_comment',
                             kwargs={'collection_id': self.collection2.id}),
                     reverse('web_collectors:update_comment',
                             kwargs={'collection_id': self.collection.id,
                                     'comment_id': self.comment.id}),
                     reverse('web_collectors:reply_comment',
                             kwargs={'collection_id': self.collection.id,
                                     'comment_id': self.comment.id}),
                     reverse('web_collectors:delete_comment',
                             kwargs={'collection_id': self.collection.id,
                                     'comment_id': self.comment.id}),
                     # reverse('web_collectors:delete_item',
                     #         kwargs={'slug': self.group.slug,
                     #                 'collection_id': self.collection.id,
                     #                 'item_id': self.collection_item.id})

                     ]

        for address in url_names:
            with self.subTest(adress=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, 200)
