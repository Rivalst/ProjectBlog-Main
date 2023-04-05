import pytest
from django.db.models import QuerySet

from django.urls import reverse
from pytest_django.asserts import assertRedirects

from blog.forms import CommentForm
from blog.models import Blog, Categories, Comment, Like, Tag


@pytest.fixture
def create_context(django_user_model):
    user = django_user_model.objects.create_user(username='Bob', password='password')

    for num in range(15):
        Blog.objects.create(author=user,
                            title=f'Title{num}',
                            text=f'Text for blog{num}'
                            )

    cat = Categories.objects.create(category='test')
    tag = Tag.objects.create(tag='test_tag')
    blog = Blog.objects.all()

    for blog in blog:
        blog.category.add(cat)
        blog.tag.add(tag)

    data_for_blog_create = {
        'title': 'title',
        'text': 'text',
        'tags': 'tags',
        'category': 'category'
    }
    context_for_comment = {
        'text': 'TestComment',
    }

    return {'blogs': blog, 'user': user, 'data': data_for_blog_create, 'comment': context_for_comment}


class TestBlogAllView:
    @pytest.mark.django_db
    def test_blog_all(self, client, create_context):
        response = client.get(reverse('blog-all'), args=create_context)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_blog_all_first_page(self, client, create_context):
        response = client.get(reverse('blog-all'), args=create_context)
        assert response.status_code == 200
        assert 'blogs' in response.context
        assert len(response.context['blogs']) == 10

    @pytest.mark.django_db
    def test_blog_all_next_page(self, client, create_context):
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


@pytest.mark.django_db
def test_blog_detail_view(client, create_context):
    blog = Blog.objects.last()
    user = create_context['user']
    client.login(username=user.username, password='password')

    if user.is_authenticated:
        blog.likes.create(user=user)

    response = client.get(reverse('blog-detail', kwargs={'pk': blog.pk}))
    context = response.context
    comments_count = blog.comments.count()
    like_count = blog.likes.count()

    assert response.status_code == 200
    assert 'comment_form' in context and isinstance(context['comment_form'], CommentForm)
    assert 'comments' in context and isinstance(context['comments'], QuerySet)
    assert len(context['comments']) == comments_count
    assert 'like_count' in context and isinstance(context['like_count'], int)
    assert context['like_count'] == like_count
    assert 'right_bar' in context and isinstance(context['right_bar'], dict)
    assert 'weather' in context and isinstance(context['weather'], dict)
    assert 'is_liked' in context and isinstance(context['is_liked'], bool)

    response_post = client.post(reverse('blog-detail', kwargs={'pk': blog.pk}), data=create_context['comment'])
    assert response_post.status_code == 302
    assert response_post.url == reverse('blog-detail', kwargs={'pk': blog.pk})

    comment = Comment.objects.last()
    assert comment.blog == blog
    assert comment.author == user
    assert comment.text == 'TestComment'
