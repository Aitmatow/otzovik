from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

CATEGORY_CHOICES = (
    ('other', 'Другое'),
    ('food', 'Еда'),
    ('clothes', 'Одежда'),
    ('household', 'Товары для дома'),
)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Товар')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0],
                                verbose_name='Категория')
    description = models.TextField(max_length=2000, verbose_name='Описание', null=True, blank=True)
    photo = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.name

    @property
    def avg_rate(self):
        avg = 0
        count = 0
        review = Review.objects.filter(product__name=self.name).filter(product__category=self.category).filter(product__description=self.description)
        for i in review:
            avg+=i.rating
            count+=1
        return '{:.2f}'.format(avg/count)


class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар')
    text = models.TextField(max_length=2000, verbose_name='Текст отзыва')
    rating = models.IntegerField(verbose_name='Оценка',validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return str(self.author) + " о товаре " + str(self.product)