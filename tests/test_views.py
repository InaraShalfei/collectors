from django.test import TestCase, Client
from django.urls import reverse

from web_collectors.models import Comment, Collection, CustomUser, CollectionGroup, CollectionItem


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
        cls.user = CustomUser.objects.create_user(username='Boba')
        cls.user2 = CustomUser.objects.create_user(username='Vera')
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
        cls.collection_item = CollectionItem.objects.create(
            name='Pushkin poems',
            description='Poems of A.S.Pushkin',
            collection=cls.collection,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        template_page_names = {
        'web_collectors/index.html': reverse('web_collectors:index'),
        'web_collectors/groups.html': reverse('web_collectors:groups'),
        'web_collectors/all_authors.html': reverse('web_collectors:all_authors'),
        'web_collectors/group.html': reverse('web_collectors:group', kwargs={'slug': 'knigi'}),
        'web_collectors/collection.html': reverse('web_collectors:collection', kwargs={
            'slug': 'knigi', 'collection_id': 1}),
        'web_collectors/item.html': reverse('web_collectors:item', kwargs={
            'slug': 'knigi', 'collection_id': 1, 'item_id': 1}),
        'web_collectors/profile.html': reverse('web_collectors:profile', kwargs={'username': 'Boba'}),
        'web_collectors/author_collection.html': reverse('web_collectors:author_collection', kwargs={
            'username': 'Boba', 'collection_id': 1}),
        'web_collectors/author_collection_item.html': reverse('web_collectors:author_collection_item', kwargs={
                                                                  'username': 'Boba', 'collection_id': 1,
                                                              'item_id': 1}),
        'includes/delete_collection.html': reverse('web_collectors:delete_collection', kwargs={
            'slug': 'knigi', 'collection_id': 1}),
        'includes/reply_comment.html': reverse('web_collectors:reply_comment', kwargs={
            'slug': 'knigi', 'collection_id': 1, 'comment_id': 1}),
        'includes/delete_comment.html': reverse('web_collectors:delete_comment', kwargs={
            'slug': 'knigi', 'collection_id': 1, 'comment_id': 1}),
        'includes/update_comment.html': reverse('web_collectors:update_comment', kwargs={
            'slug': 'knigi', 'collection_id': 1, 'comment_id': 1}),
        'web_collectors/new_item.html': reverse('web_collectors:new_item', kwargs={'slug': 'knigi',
                                                                                   'collection_id': 1}),
        'includes/delete_item.html': reverse('web_collectors:delete_item', kwargs={
            'slug': 'knigi', 'collection_id': 1, 'item_id': 1}),
        'web_collectors/follow.html': reverse('web_collectors:follow_index'),
        'includes/unfollow.html': reverse('web_collectors:profile_unfollow', kwargs={'username': 'Boba'}),
        }
        for template, reverse_name in template_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
