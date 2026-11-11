from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.core.exceptions import ValidationError


class Config(models.Model):
    contact_phone = models.CharField(max_length=100, blank=True, default='')
    contact_phone_2 = models.CharField(max_length=100, blank=True, default='')
    contact_phone_3 = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    email_2 = models.EmailField(blank=True, default='')
    instagram_link = models.CharField(max_length=255, blank=True, default='')
    facebook_link = models.CharField(max_length=255, blank=True, default='')
    tiktok_link = models.CharField(max_length=255, blank=True, default='')
    youtube_link = models.CharField(max_length=255, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default='Pridruži se školama Realnog Aikidoa u Beogradu i nauči veštinu samoodbrane za stvarni svet.',
    )
    about_blurb = models.TextField(
        blank=True,
        default=(
            'Realni aikido je savremeni sistem samoodbrane nastao u Srbiji. '
            'Spoj tradicionalnih japanskih principa i praktičnih tehnika za svakodnevne situacije.'
        ),
    )

    class Meta:
        verbose_name = 'Konfiguracija sajta'
        verbose_name_plural = 'Konfiguracija sajta'

    def save(self, *args, **kwargs):
        if not self.pk and Config.objects.exists():
            raise ValidationError('Može postojati samo jedna konfiguracija sajta.')
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Konfiguracija sajta'

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj


class Instructor(models.Model):
    BELT_CHOICES = [
        ('1.dan', 'Crni pojas 1. dan'),
        ('2.dan', 'Crni pojas 2. dan'),
        ('3.dan', 'Crni pojas 3. dan'),
        ('4.dan', 'Crni pojas 4. dan'),
        ('5.dan', 'Crni pojas 5. dan'),
    ]

    TITLE_CHOICES = [
        ('glavni_majstor', 'Glavni majstor'),
        ('predsednik', 'Predsednik'),
        ('instruktor', 'Instruktor'),
    ]

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, choices=TITLE_CHOICES, help_text='Zvanje instruktora')
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    belt_rank = models.CharField(max_length=20, choices=BELT_CHOICES)
    photo = models.ImageField(upload_to='instructors/')
    slug = models.SlugField(unique=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f'{self.name} {self.belt_rank}')
            slug = base_slug
            counter = 1
            while Instructor.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150, blank=True, default='')
    bio = models.TextField(blank=True, default='')
    photo = models.ImageField(upload_to='masters/', blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Majstor'
        verbose_name_plural = 'Majstori'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, default='')
    trainer_name = models.CharField(max_length=100, blank=True, default='')
    trainer_belt = models.CharField(max_length=100, blank=True, default='')
    map_embed_url = models.URLField(max_length=500, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Lokacija'
        verbose_name_plural = 'Lokacije'

    def __str__(self):
        return self.name

    @property
    def maps_url(self):
        url = (self.map_embed_url or '').strip()
        if url:
            return (
                url
                .replace('&output=embed', '')
                .replace('?output=embed', '')
                .rstrip('?&')
            )
        if self.address:
            from urllib.parse import quote_plus
            return f'https://www.google.com/maps/search/?api=1&query={quote_plus(self.address)}'
        return ''

    @property
    def tel_href(self):
        digits = ''.join(ch for ch in (self.phone or '') if ch.isdigit() or ch == '+')
        return f'tel:{digits}' if digits else ''


class LocationGroup(models.Model):
    GROUP_TYPES = [
        ('younger', 'Mlađa grupa'),
        ('older', 'Starija grupa'),
        ('adults', 'Odrasli'),
        ('other', 'Ostalo'),
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='groups')
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES, default='other')
    label = models.CharField(max_length=100)
    days = models.CharField(max_length=100, help_text='npr. Utorak i Četvrtak')
    time_range = models.CharField(max_length=100, help_text='npr. 19:30 DO 20:30')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Grupa na lokaciji'
        verbose_name_plural = 'Grupe na lokaciji'

    def __str__(self):
        return f'{self.location.name} — {self.label}'


class Program(models.Model):
    AUDIENCE_CHOICES = [
        ('kids', 'Za decu'),
        ('adults', 'Za odrasle'),
    ]

    title = models.CharField(max_length=100)
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']
        verbose_name = 'Program'
        verbose_name_plural = 'Programi'

    def __str__(self):
        return self.title


class ProgramBelt(models.Model):
    COLOR_CHOICES = [
        ('yellow', 'Žuti'),
        ('orange', 'Narandžasti'),
        ('green', 'Zeleni'),
        ('blue', 'Plavi'),
        ('brown', 'Braon'),
        ('black', 'Crni'),
    ]

    COLOR_CLASSES = {
        'yellow': 'bg-yellow-200',
        'orange': 'bg-orange-500',
        'green': 'bg-green-500',
        'blue': 'bg-blue-500',
        'brown': 'bg-amber-800',
        'black': 'bg-black',
    }

    COLOR_ACTIVE_CLASSES = {
        'yellow': 'bg-yellow-100 ring-2 ring-yellow-400 text-ink shadow-sm',
        'orange': 'bg-orange-100 ring-2 ring-orange-400 text-ink shadow-sm',
        'green': 'bg-green-100 ring-2 ring-green-500 text-ink shadow-sm',
        'blue': 'bg-blue-100 ring-2 ring-blue-400 text-ink shadow-sm',
        'brown': 'bg-amber-100 ring-2 ring-amber-700 text-ink shadow-sm',
        'black': 'bg-stone-200 ring-2 ring-stone-500 text-ink shadow-sm',
    }

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='belts')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='yellow')
    description = models.TextField(help_text='Opis tehnika / kurikuluma (može HTML)')
    youtube_id = models.CharField(max_length=32, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Pojas u programu'
        verbose_name_plural = 'Pojasevi u programu'

    def __str__(self):
        return f'{self.program.title} — {self.name}'

    @property
    def color_class(self):
        return self.COLOR_CLASSES.get(self.color, 'bg-gray-400')

    @property
    def color_active_class(self):
        return self.COLOR_ACTIVE_CLASSES.get(self.color, 'bg-stone-100 ring-1 ring-stone-300 text-ink')


class TimelineEvent(models.Model):
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'year']
        verbose_name = 'Događaj istorijata'
        verbose_name_plural = 'Istorijat'

    def __str__(self):
        return f'{self.year} — {self.title or self.description[:40]}'


class Blog(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    main_image = models.ImageField(upload_to='blog/main_images/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def images(self):
        blog_content_type = ContentType.objects.get_for_model(self)
        return Image.objects.filter(content_type=blog_content_type, object_id=self.id)


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


class Product(models.Model):
    name = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='products/main_images/')
    description = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)
    sku = models.CharField(max_length=64, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, blank=True)
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
    def related_products(self):
        return Product.objects.filter(category=self.category).exclude(id=self.id)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=255, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption or "Image"} for {self.content_object}'
