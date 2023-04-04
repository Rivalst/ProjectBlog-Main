from django.db.models import Count

from blog.models import Tag, Categories


def tag_get_or_create(tags: list, blog):
    for tag in tags:
        if tag.strip():
            tag_object, _ = Tag.objects.get_or_create(tag=tag.strip())
            tag_object.blog.add(blog)

    Tag.objects.annotate(blog_count=Count('blog')).filter(blog_count=0).delete()


def category_get_or_create(category: str, blog):
    category = ' '.join(category.split())
    category_object, _ = Categories.objects.get_or_create(category=category.strip())
    category_object.blog.add(blog)

    Categories.objects.annotate(blog_count=Count('blog')).filter(blog_count=0).delete()
