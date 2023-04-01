from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(default='blog-post-01.jpg', upload_to='blog_avatars')

    def __str__(self):
        return f'{self.title} by: {self.author}'

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.text[:50]}'


class Tag(models.Model):
    blog = models.ManyToManyField(Blog, related_name='tag')
    tag = models.CharField(max_length=150)

    def __str__(self):
        return self.tag


class Categories(models.Model):
    blog = models.ManyToManyField(Blog, related_name='category')
    category = models.CharField(max_length=150)

    def __str__(self):
        return self.category


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.blog}'
