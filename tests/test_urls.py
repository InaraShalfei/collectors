from django.test import TestCase, Client

from web_collectors.models import Comment, Collection, CustomUser, CollectionGroup, CollectionItem


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

    def test_urls_exist_at_desired_location_for_guest_client(self):
        url_names = ['', '/groups/',  '/all/', '/group/knigi/',
                     '/group/knigi/1', '/group/knigi/1/1',
                     '/profile/Boba/', '/profile/Boba/1', '/profile/Boba/1/1']

        for address in url_names:
            with self.subTest(adress=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200)

    # def test_urls_exist_at_desired_location_for_authorized_client(self):
    #     url_names = ['/new_collection/', '/group/knigi/1/delete', '/group/knigi/1/1/reply',
    #                  '/group/knigi/1/1/delete_comment', '/group/knigi/1/1/update_comment',
    #                  '/group/knigi/1/new', '/group/knigi/1/1/delete',  '/follow/']
    #
    #     for address in url_names:
    #         with self.subTest(adress=address):
    #             response = self.authorized_client.get(address)
    #             self.assertEqual(response.status_code, 200)

    def test_pages_for_guest_client_have_correct_templates(self):
        templates_url_names = {
        'web_collectors/index.html': '',
        'web_collectors/groups.html': '/groups/',
        'web_collectors/all_authors.html': '/all/',
        'web_collectors/group.html': '/group/knigi/',
        'web_collectors/collection.html': '/group/knigi/1',
        'web_collectors/item.html': '/group/knigi/1/1',
        'web_collectors/profile.html': '/profile/Boba/',
        'web_collectors/author_collection.html': '/profile/Boba/1',
        'web_collectors/author_collection_item.html': '/profile/Boba/1/1',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_pages_for_authorized_client_have_correct_templates(self):
        templates_url_names = {
        'includes/delete_collection.html': '/group/knigi/1/delete',
        'includes/reply_comment.html': '/group/knigi/1/1/reply',
        'includes/delete_comment.html': '/group/knigi/1/1/delete_comment',
        'includes/update_comment.html': '/group/knigi/1/1/update_comment',
        'web_collectors/new_item.html': '/group/knigi/1/new',
        'includes/delete_item.html': '/group/knigi/1/1/delete',
        'web_collectors/follow.html': '/follow/',
        'includes/unfollow.html': '/profile/Boba/unfollow',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    # def test_redirects_for_anonymous(self):
    #     url_names = ['/group/knigi/1/comment', '/new_collection/', '/group/knigi/1/edit',
    #                  '/group/knigi/1/delete', '/group/knigi/1/1/reply', '/group/knigi/1/1/delete_comment',
    #                  '/group/knigi/1/1/update_comment', '/group/knigi/1/new', '/group/knigi/1/1/update',
    #                  '/group/knigi/1/1/delete', '/follow/', '/profile/Boba/follow', '/profile/Boba/unfollow']
    #     for address in url_names:
    #         with self.subTest(address=address):
    #             response = self.guest_client.get(address, follow=True)
    #             self.assertRedirects(response, f'/auth/login/?next={address}')

