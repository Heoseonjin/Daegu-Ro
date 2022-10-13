from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/recommend/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

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

    def get_absolute_url(self):
        return f'/recommend/{self.pk}'