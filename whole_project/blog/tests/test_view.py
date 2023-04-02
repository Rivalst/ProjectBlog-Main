import functools

from django.test import TestCase
from django.urls import reverse

from blog.models import Blog, User, Categories


class BlogAllViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(category='Top')
        cls.user_blog = User.objects.create_user(username='Bob', password='password')
        num_of_blog = 15
        for num in range(num_of_blog):
            Blog.objects.create(
                author=cls.user_blog,
                title='Title',
                text='Text for blog',

            )

        blog = Blog.objects.all()
        for blog in blog:
            blog.category.add(cls.category)

    def test_url_exist(self):
        response = self.client.get(reverse('blog-all'))
        self.assertEquals(response.status_code, 200)

    def test_is_pagination_first_page(self):
        response = self.client.get(reverse('blog-all'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('blogs' in response.context)
        self.assertTrue(len(response.context['blogs']) == 10)

    def test_is_pagination_next_page(self):
        response = self.client.get(reverse('blog-all') + '?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('blogs' in response.context)
        self.assertTrue(len(response.context['blogs']) == 5)
