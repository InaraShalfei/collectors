from django.test import TestCase

from web_collectors.models import CollectionGroup


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


