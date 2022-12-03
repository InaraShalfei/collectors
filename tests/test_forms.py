import shutil
import tempfile


from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase, Client
from django.urls import reverse

from web_collectors.forms import CollectionForm, CommentForm, ItemForm
from web_collectors.models import (Collection, CollectionGroup, CustomUser,
                                   Comment, CollectionItem)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


def get_fake_image():
    return SimpleUploadedFile(
        name='small.gif',
        content=(
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        ),
        content_type='image/gif'
    )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CollectionFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serialized_rollback = True
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(username='User')
        CollectionGroup.objects.create(
            name='Фильмы',
            slug='films',
            description='All films in the world'
        )
        cls.form = CollectionForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_collection(self):
        collection_count = Collection.objects.count()
        form_data = {
            'name': 'Russian films',
            'description': 'All films of russian authors',
            'photo': get_fake_image(),
            'group': 1
        }
        response = self.authorized_client.post(
            reverse('web_collectors:new_collection'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Collection.objects.count(), collection_count+1)
        self.assertEqual(response.status_code, 200)

    def test_cant_create_collection_without_name(self):
        collection_count = Collection.objects.count()
        form_data = {
            'name': '',
            'description': 'New cool film',
            'photo': get_fake_image(),
            'group': 1
        }
        response = self.authorized_client.post(
            reverse('web_collectors:new_collection'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Collection.objects.count(), collection_count)
        self.assertEqual(response.status_code, 200)


class CommentFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serialized_rollback = True
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(username='User1',
                                                  email='user1@mail.kz')
        cls.user2 = CustomUser.objects.create_user(username='User2',
                                                   email='user2@mail.kz')
        group = CollectionGroup.objects.create(
            name='Фильмы-2',
            slug='films-2',
            description='All films in the world - 2'
        )
        cls.collection = Collection.objects.create(
            name='Russian poems',
            description='All Russian poems',
            owner=cls.user,
            group=group)

        cls.form = CommentForm()
        cls.comment = Comment.objects.create(
            collection=cls.collection,
            author=cls.user2,
            text='Cool!',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_comment(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Super-puper!'
        }
        response = self.authorized_client.post(
            reverse('web_collectors:add_comment',
                    kwargs={'collection_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), comment_count+1)

    def test_reply_comment(self):
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Thanks!!'
        }
        response = self.authorized_client.post(
            reverse('web_collectors:reply_comment',
                    kwargs={'collection_id': 1,
                            'comment_id': self.comment.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), comment_count+1)


class ItemFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serialized_rollback = True
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(username='User2')
        group = CollectionGroup.objects.create(
            name='Фильмы-3',
            slug='films-3',
            description='All films in the world - 3'
        )
        collection = Collection.objects.create(
            name='Russian poems-2',
            description='All Russian poems-2',
            owner=cls.user,
            group=group)
        CollectionItem.objects.create(
            name='Poem by Pushkin',
            description='Poem written by Pushkin',
            collection=collection
        )

        cls.form = ItemForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_new_item(self):
        item_count = CollectionItem.objects.count()
        form_data = {
            'name': 'New_item',
            'description': 'very good new item',
            'photos': [get_fake_image()]
        }
        response = self.authorized_client.post(
            reverse('web_collectors:new_item',
                    kwargs={'slug': 'films-3', 'collection_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(CollectionItem.objects.count(), item_count+1)

    def test_cant_create_item_without_name(self):
        item_count = CollectionItem.objects.count()
        form_data = {
            'name': '',
            'description': 'very good new item-2',
            'photo': [get_fake_image()]
        }
        response = self.authorized_client.post(
            reverse('web_collectors:new_item',
                    kwargs={'slug': 'films-3', 'collection_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(CollectionItem.objects.count(), item_count)
        self.assertEqual(response.status_code, 422)
