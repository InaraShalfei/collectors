from django.test import TestCase, Client
from django.urls import reverse

from web_collectors.models import (Comment, Collection, CustomUser,
                                   CollectionGroup, CollectionItem, Follow)


class CollectionViewsTest(TestCase):
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
                                                  email='boba@boba.com')
        cls.user2 = CustomUser.objects.create_user(username='Vera',
                                                   email='vera@vera.com')
        cls.collection = Collection.objects.create(
            name='Russian authors',
            description='All books of russian authors',
            owner=cls.user,
            group=cls.group
        )
        cls.comment = Comment.objects.create(
            collection=cls.collection,
            author=cls.user2,
            text='Cool!',
        )
        cls.comment_answer = Comment.objects.create(
            collection=cls.collection,
            author=cls.user,
            text='Thanks!',
            parent_comment=cls.comment
        )
        cls.collection_item = CollectionItem.objects.create(
            name='Pushkin poems',
            description='Poems of A.S.Pushkin',
            collection=cls.collection,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_simple_pages_use_correct_template(self):
        template_page_names = {
            'web_collectors/index.html': reverse('web_collectors:index'),
            # 'web_collectors/search.html': reverse('web_collectors:search',
            #                                       kwargs={'collection_name':self.collection.name}),
            'web_collectors/groups.html': reverse('web_collectors:groups'),
            'web_collectors/all_authors.html':
                reverse('web_collectors:all_authors'),
            'web_collectors/group.html': reverse('web_collectors:group',
                                                 kwargs={'slug': 'knigi'}),
            'web_collectors/collection.html':
                reverse('web_collectors:collection',
                        kwargs={'slug': 'knigi', 'collection_id': 1}),
            'web_collectors/item.html':
                reverse('web_collectors:item',
                        kwargs={'slug': 'knigi', 'collection_id': 1,
                                'item_id': 1}),
            'web_collectors/profile.html':
                reverse('web_collectors:profile', kwargs={'username': 'Boba'}),
            'web_collectors/author_collection.html':
                reverse('web_collectors:author_collection',
                        kwargs={'username': 'Boba', 'collection_id': 1}),
            'web_collectors/author_collection_item.html':
                reverse('web_collectors:author_collection_item',
                        kwargs={'username': 'Boba', 'collection_id': 1,
                                'item_id': 1}),
            'web_collectors/follow.html':
                reverse('web_collectors:follow_index'),

        }
        for template, reverse_name in template_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_collection_page_render_all_templates(self):
        reverse_names = [reverse('web_collectors:collection',
                                 kwargs={'slug': self.group.slug,
                                         'collection_id': 1}),
                         reverse('web_collectors:author_collection',
                                 kwargs={'username': self.user.username,
                                         'collection_id': self.collection.id})
                         ]
        template_page_names = {'includes/reply_comment.html': reverse_names,
                               'includes/delete_comment.html': reverse_names,
                               'includes/update_comment.html': reverse_names,
                               'includes/child_comments.html': reverse_names,
                               'includes/new_item.html': reverse_names,
                               'includes/create_collection.html': reverse_names,
                               'includes/favorite.html': reverse_names
                               }
        comment = Comment.objects.create(
            collection=self.collection,
            author=self.user2,
            text='Cool!',
        )
        comment.save()

        for template, reverse_names in template_page_names.items():
            for reverse_name in reverse_names:
                with self.subTest(reverse_name=reverse_name):
                    response = self.authorized_client.get(reverse_name)
                    self.assertTemplateUsed(response, template)

    def test_group_page_render_all_templates(self):
        reverse_name = reverse('web_collectors:group',
                               kwargs={'slug': self.group.slug})

        template_page_names = {
                               'includes/create_collection.html': reverse_name,
                               'includes/delete_collection.html': reverse_name
                               }

        for template, reverse_names in template_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_profile_page_render_all_templates(self):
        reverse_name = reverse('web_collectors:profile',
                               kwargs={'username': self.user.username})

        following = Follow.objects.create(user=self.user2, author=self.user)
        following.save()

        template_page_names = {
                               'includes/create_collection.html': reverse_name,
                               'includes/delete_collection.html': reverse_name,
                               'includes/author_card.html': reverse_name,
                               # 'includes/unfollow.html': reverse_name,
                               # 'includes/follow.html': reverse_name
                               }

        for template, reverse_names in template_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


    # 'includes/delete_item.html': reverse('web_collectors:delete_item',
    #                                      kwargs={'slug': 'knigi',
    #                                              'collection_id': 1,
    #                                              'item_id': 1}),
    # 'includes/follow.html': reverse('web_collectors:profile',kwargs={'username': 'Vera'}),
    # 'includes/unfollow.html': reverse('web_collectors:profile',kwargs={'username': 'Vera'})
