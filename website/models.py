from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


class Config(models.Model):
    contact_phone = models.CharField(max_length=100, blank=True, null=True, default='061')
    email = models.EmailField(blank=True, null=True, default='default@default.com')
    instagram_link = models.CharField(max_length=255, blank=True, null=True, default='www.instagram.com')
    facebook_link = models.CharField(max_length=255, blank=True, null=True, default='www.facebook.com')
    tiktok_link = models.CharField(max_length=255, blank=True, null=True, default='www.tiktok.com')
    youtube_link = models.CharField(max_length=255, blank=True, null=True, default='www.youtube.com')
    address = models.CharField(max_length=255, blank=True, null=True, default='default address')


class Instructor(models.Model):
    BELT_CHOICES = [
        ('1.dan', 'Crni pojas 1. dan'),
        ('2.dan', 'Crni pojas 2. dan'),
        ('3.dan', 'Crni pojas 3. dan'),
        ('4.dan', 'Crni pojas 4. dan'),
        ('5.dan', 'Crni pojas 5. dan'),
        # dodaj više ako treba
    ]

    TITLE_CHOICES = [
        ('glavni_majstor', 'Glavni majstor'),
        ('predsednik', 'Predsednik'),
        ('instruktor', 'Instruktor'),
    ]
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100,choices=TITLE_CHOICES, help_text="Zvanje instruktora")
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    belt_rank = models.CharField(max_length=20, choices=BELT_CHOICES)
    photo = models.ImageField(upload_to='instructors/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):

        if not self.slug:
            # napravi slug iz name + belt_rank
            base_slug = f"{self.name} {self.belt_rank}"
            self.slug = slugify(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    main_image = models.ImageField(upload_to='blog/main_images/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # napravi slug iz name + belt_rank
            base_slug = f"{self.title}"
            self.slug = slugify(base_slug)
        super().save(*args, **kwargs)

    @property
    def images(self):
        blog_content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(content_type=blog_content_type, object_id=self.id)


class Product(models.Model):
    name = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='products/main_images/')
    description = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)
    sku = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, blank=True)  # opcionalno, za SEO-friendly URL

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def images(self):
        product_content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(content_type=product_content_type, object_id=self.id)

    @property
    def get_related_products(self):
        return Product.objects.filter(
            category=self.category
        ).exclude(id=self.id)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=255, blank=True)

    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_main = models.BooleanField(default=False)  # True ako je glavna slika
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.caption or 'Image'} for {self.content_object}"
