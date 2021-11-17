import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase, Client
from django.urls import reverse

from web_collectors.forms import CollectionForm, CommentForm
from web_collectors.models import Collection, CollectionGroup, User, Comment

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CollectionFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serialized_rollback = True
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')
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
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'name': 'Russian films',
            'description': 'All films of russian authors',
            'photo': uploaded,
            'group': 1
        }
        response = self.authorized_client.post(
            reverse('web_collectors:new_collection'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('web_collectors:collection', kwargs={'slug': 'films', 'collection_id': 1}))
        self.assertEqual(Collection.objects.count(), collection_count+1)

    def test_cant_create_collection_without_name_and_description(self):
        collection_count = Collection.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'name': '',
            'description': 'New cool film',
            'photo': uploaded,
            'group': 1
        }
        response = self.authorized_client.post(
            reverse('web_collectors:new_collection'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Collection.objects.count(), collection_count)
        self.assertFormError(response, 'form', 'name', 'Обязательное поле.')
        self.assertEqual(response.status_code, 200)


class CommentFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serialized_rollback = True
        super().setUpClass()
        cls.user = User.objects.create_user(username='User1')
        group = CollectionGroup.objects.create(
            name='Фильмы-2',
            slug='films-2',
            description='All films in the world -2'
        )
        Collection.objects.create(
            name='Russian poems',
            description='All Russian poems',
            owner=cls.user,
            group=group)

        cls.form = CommentForm()

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
                    kwargs={'slug': 'films-2', 'collection_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('web_collectors:collection', kwargs={'slug': 'films-2', 'collection_id': 1}))
        self.assertEqual(Comment.objects.count(), comment_count+1)







