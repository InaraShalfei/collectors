from django.db.utils import IntegrityError

from django.test import TestCase

from web_collectors.models import CollectionGroup, Collection, User, CollectionItem, Comment, Follow


class CollectionGroupTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = CollectionGroup.objects.create(
            name='Книги',
            slug='',
            description='All books in the world'
        )

    def test_verbose_names(self):
        group = CollectionGroupTest.group
        field_verboses = {
            'name': 'Название группы',
            'slug': 'Адрес страницы с группой коллекций',
            'description': 'Описание группы'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(group._meta.get_field(field).verbose_name, expected_value)

    def test_name_field_is_str(self):
        group = CollectionGroupTest.group
        expected_name = group.name
        self.assertEqual(expected_name, str(group))

    def test_convert_to_slug(self):
        group = CollectionGroupTest.group
        slug = group.slug
        self.assertEqual(slug, 'knigi')

    def test_slug_length_not_exceed(self):
        group = CollectionGroupTest.group
        max_length = group._meta.get_field('slug').max_length
        length = len(group.slug)*10
        self.assertEqual(max_length, length)


class CollectionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = CollectionGroup.objects.create(
            name='Книги',
            slug='',
            description='All books in the world'
        )
        cls.user = User.objects.create_user(username='auth')
        cls.collection = Collection.objects.create(
            name='Russian authors',
            description='All books of russian authors',
            owner=cls.user,
            group=cls.group
        )

    def test_verbose_names(self):
        collection = CollectionTest.collection
        field_verboses = {
            'name': 'Название коллекции',
            'description': 'Описание коллекции',
            'owner': 'Создатель коллекции',
            'group': 'Группа коллекций'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(collection._meta.get_field(field).verbose_name, expected_value)

    def test_name_field_is_str(self):
        collection = CollectionTest.collection
        expected_name = collection.name
        self.assertEqual(expected_name, str(collection))


class CollectionItemTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = CollectionGroup.objects.create(
            name='Книги',
            slug='',
            description='All books in the world'
        )
        cls.user = User.objects.create_user(username='auth')
        cls.collection = Collection.objects.create(
            name='Russian authors',
            description='All books of russian authors',
            owner=cls.user,
            group=cls.group
        )
        cls.collection_item = CollectionItem.objects.create(
            name='Pushkin poems',
            description='Poems of A.S.Pushkin',
            collection=cls.collection,
        )

    def test_verbose_names(self):
        collection_item = CollectionItemTest.collection_item
        field_verboses = {
            'name': 'Название объекта коллекции',
            'description': 'Описание объекта коллекции',
            'collection': 'Коллекция объектов'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(collection_item._meta.get_field(field).verbose_name, expected_value)

    def test_name_field_is_str(self):
        collection_item = CollectionItemTest.collection_item
        expected_name = collection_item.name
        self.assertEqual(expected_name, str(collection_item))


class CommentTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = CollectionGroup.objects.create(
            name='Книги',
            slug='',
            description='All books in the world'
        )
        cls.user = User.objects.create_user(username='auth')
        cls.collection = Collection.objects.create(
            name='Russian authors',
            description='All books of russian authors',
            owner=cls.user,
            group=cls.group
        )
        cls.comment = Comment.objects.create(
            collection=cls.collection,
            author=cls.user,
            text='Cool!',
        )

    def test_verbose_names(self):
        comment = CommentTest.comment
        field_verboses= {
            'collection': 'Название коллекции',
            'author': 'Автор коллекции',
            'text': 'Текст комментария',
            'parent_comment': 'Ответный комментарий'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(comment._meta.get_field(field).verbose_name, expected_value)

    def test_text_is_str(self):
        comment = CommentTest.comment
        expected_value = comment.text
        self.assertEqual(expected_value, str(comment))


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='arm')
        cls.user2 = User.objects.create_user(username='bcd')
        cls.follow = Follow.objects.create(
            user=cls.user1,
            author=cls.user2
        )

    def test_verbose_names(self):
        follow = FollowTest.follow
        field_verboses = {
            'user': 'Подписчик',
            'author': 'Автор коллекции'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(follow._meta.get_field(field).verbose_name, expected_value)

    def test_unique_constraint_relation(self):
        user_1 = User.objects.create(username='123')
        user_2 = User.objects.create(username='345')
        Follow.objects.create(user=user_1, author=user_2)
        follow = Follow(user=user_1, author=user_2)
        with self.assertRaises(Exception) as raised:
            follow.save()
        self.assertEqual(IntegrityError, type(raised.exception))
