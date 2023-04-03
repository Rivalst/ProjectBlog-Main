import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from blog.models import Blog, Categories


@pytest.fixture
def create_context(django_user_model):
    user = django_user_model.objects.create_user(username='Bob', password='password')

    for num in range(15):
        Blog.objects.create(author=user,
                            title='Title',
                            text='Text for blog'
                            )

    cat = Categories.objects.create(category='test')
    blog = Blog.objects.all()

    for blog in blog:
        blog.category.add(cat)

    data_for_blog_create = {
        'title': 'title',
        'text': 'text',
        'tags': 'tags',
        'category': 'category'
    }

    return {'blogs': blog, 'user': user, 'data': data_for_blog_create}


@pytest.mark.django_db
def test_blog_all_view(client, create_context):
    response = client.get(reverse('blog-all'), args=create_context)
    assert response.status_code == 200


@pytest.mark.django_db
def test_blog_all_first_page_view(client, create_context):
    response = client.get(reverse('blog-all'), args=create_context)
    assert response.status_code == 200
    assert 'blogs' in response.context
    assert len(response.context['blogs']) == 10


@pytest.mark.django_db
def test_blog_all_next_page_view(client, create_context):
    response = client.get(reverse('blog-all') + '?page=2', args=create_context)
    assert response.status_code == 200
    assert 'blogs' in response.context
    assert len(response.context['blogs']) == 5


@pytest.mark.django_db
def test_blog_create_view(client, create_context):
    client.force_login(create_context['user'])

    response_get = client.get(reverse('blog-create'))
    assert response_get.status_code == 200

    response_post = client.post(reverse('blog-create'), data=create_context['data'])
    assertRedirects(response_post, reverse('home'), status_code=302)

    blog_post = Blog.objects.last()

    assert blog_post.tag.all().exists()
    assert blog_post.category.all().exists()
    assert blog_post.title == create_context['data']['title']
    assert blog_post.text == create_context['data']['text']
    assert Blog.objects.last().author == create_context['user']
