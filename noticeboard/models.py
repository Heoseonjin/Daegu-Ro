from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/board/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 삭제된 작성자 None 표시
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 카테고리 필드
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/board/{self.pk}'

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment={self.pk}'
        
    # 구글 아바타 설정하기
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1275/d558eb306b1ea8e0/svg/{{ self.author.email }}'




# 지울 것인가 말 것인가. recommend app에서 실패하면 도전해보기

class Recommend(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=50)
    contents = models.CharField(max_length=5000)

    lat = models.DecimalField(max_digits=11, decimal_places=5)
    lon = models.DecimalField(max_digits=11, decimal_places=5)

    # 카테고리 필드
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.category}] - {self.name}'
