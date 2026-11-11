import logging
import re

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.http import require_GET, require_http_methods

from .forms import ContactForm
from .models import (
    Blog,
    Category,
    Config,
    Instructor,
    Location,
    Master,
    Product,
    Program,
    TimelineEvent,
)

logger = logging.getLogger('website')


def _blog_intro_and_body(description):
    """Split blog copy into lead + body; avoid duplicating short posts."""
    raw = (description or '').strip()
    if not raw:
        return '', '', False

    if re.search(r'<(p|div|h[1-6]|ul|ol|blockquote)\b', raw, re.I):
        paragraphs = re.findall(r'<p\b[^>]*>(.*?)</p>', raw, flags=re.I | re.S)
        has_other_blocks = bool(re.search(r'<(h[1-6]|ul|ol|blockquote)\b', raw, re.I))
        if len(paragraphs) >= 2 and not has_other_blocks:
            first = re.search(r'<p\b[^>]*>.*?</p>', raw, flags=re.I | re.S)
            intro = strip_tags(first.group(0)).strip()
            body = raw[first.end():].strip()
            return intro, body, True
        if len(paragraphs) == 1 and not has_other_blocks:
            return strip_tags(raw).strip(), '', False
        return '', raw, True

    parts = [part.strip() for part in re.split(r'\n\s*\n+', raw) if part.strip()]
    if len(parts) <= 1:
        return raw, '', False
    return parts[0], '\n\n'.join(parts[1:]), False


def home(request):
    instructors = Instructor.objects.filter(is_active=True)[:3]
    config = Config.get_solo()

    blog_qs = Blog.objects.all().order_by('-date', '-id')
    blog_featured = None
    if any(f.name == 'is_featured' for f in Blog._meta.get_fields()):
        blog_featured = blog_qs.filter(is_featured=True).first()
    if blog_featured is None:
        blog_featured = blog_qs.first()
    blog_side = []
    if blog_featured is not None:
        blog_side = list(blog_qs.exclude(pk=blog_featured.pk)[:2])

    return render(request, 'website/pages/index.html', {
        'instructors': instructors,
        'config': config,
        'blog_featured': blog_featured,
        'blog_side': blog_side,
    })


def programs(request):
    programs_qs = Program.objects.filter(is_active=True).prefetch_related('belts')
    return render(request, 'website/pages/programs.html', {
        'programs': programs_qs,
    })


def instructors(request):
    instructors_qs = Instructor.objects.filter(is_active=True)
    return render(request, 'website/pages/instructors.html', {
        'instructors': instructors_qs,
    })


def instructor(request, slug):
    instructor_obj = get_object_or_404(Instructor, slug=slug, is_active=True)
    return render(request, 'website/pages/single_instructor.html', {
        'instructor': instructor_obj,
    })


def locations(request):
    locations_qs = Location.objects.filter(is_active=True).prefetch_related('groups')
    return render(request, 'website/pages/locations.html', {
        'locations': locations_qs,
    })


def blog(request):
    posts_qs = Blog.objects.all().order_by('-date', '-id')
    featured = None
    if any(f.name == 'is_featured' for f in Blog._meta.get_fields()):
        featured = posts_qs.filter(is_featured=True).first()
    if featured is None:
        featured = posts_qs.first()
    rest = []
    if featured is not None:
        rest = list(posts_qs.exclude(pk=featured.pk))
    return render(request, 'website/pages/blog.html', {
        'blog_featured': featured,
        'blog_rest': rest,
    })


def post(request, slug):
    post_obj = get_object_or_404(Blog, slug=slug)
    post_intro, post_body, post_body_is_html = _blog_intro_and_body(post_obj.description)
    return render(request, 'website/pages/post.html', {
        'post': post_obj,
        'post_intro': post_intro,
        'post_body': post_body,
        'post_body_is_html': post_body_is_html,
    })


def masters(request):
    masters_qs = Master.objects.filter(is_active=True)
    return render(request, 'website/pages/masters.html', {
        'masters': masters_qs,
    })


def shop(request):
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(request, 'website/pages/shop.html', {
        'products': products,
        'active_category': category_slug,
        'categories': Category.objects.all(),
    })


def product(request, slug):
    product_obj = get_object_or_404(Product, slug=slug)
    return render(request, 'website/pages/single_product.html', {
        'product': product_obj,
        'related_products': product_obj.related_products,
    })


def product_legacy_redirect(request, slug):
    return redirect('product', slug=slug, permanent=True)


def timeline(request):
    events = TimelineEvent.objects.filter(is_active=True).order_by('year', 'sort_order', 'id')
    return render(request, 'website/pages/timeline.html', {
        'events': events,
    })


@require_http_methods(['GET', 'POST'])
def contact(request):
    config = Config.get_solo()
    locations_qs = Location.objects.filter(is_active=True).prefetch_related('groups')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_body = form.cleaned_data['message']
            subject = f'Kontakt forma — {name}'
            body = f'Ime: {name}\nEmail: {email}\n\n{message_body}'
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [getattr(settings, 'CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)],
                    fail_silently=False,
                )
                logger.info('Contact form submitted by %s <%s>', name, email)
                messages.success(request, 'Poruka je uspešno poslata. Javićemo vam se uskoro.')
                return redirect('contact')
            except Exception:
                logger.exception('Failed to send contact email from %s', email)
                messages.error(request, 'Slanje nije uspelo. Pokušajte ponovo ili nas pozovite.')
        else:
            messages.error(request, 'Proverite unete podatke.')
    else:
        form = ContactForm()

    return render(request, 'website/pages/contact.html', {
        'form': form,
        'config': config,
        'locations': locations_qs,
    })


def _absolute_url(path):
    return f"{settings.SITE_URL}{path}"


@require_GET
def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        f'Sitemap: {_absolute_url("/sitemap.xml")}',
        '',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')


@require_GET
def sitemap_xml(request):
    static_pages = [
        ('home', '1.0', 'weekly'),
        ('locations', '0.9', 'weekly'),
        ('programs', '0.9', 'monthly'),
        ('instructors', '0.8', 'monthly'),
        ('blog', '0.8', 'weekly'),
        ('contact', '0.7', 'monthly'),
        ('timeline', '0.5', 'yearly'),
        ('masters', '0.5', 'yearly'),
    ]

    urls = []
    for name, priority, changefreq in static_pages:
        urls.append({
            'loc': _absolute_url(reverse(name)),
            'priority': priority,
            'changefreq': changefreq,
        })

    for instructor in Instructor.objects.filter(is_active=True):
        urls.append({
            'loc': _absolute_url(reverse('instructor', kwargs={'slug': instructor.slug})),
            'priority': '0.6',
            'changefreq': 'monthly',
            'lastmod': instructor.updated_at.date().isoformat() if getattr(instructor, 'updated_at', None) else None,
        })

    for post_obj in Blog.objects.all():
        urls.append({
            'loc': _absolute_url(reverse('post', kwargs={'slug': post_obj.slug})),
            'priority': '0.7',
            'changefreq': 'monthly',
            'lastmod': (
                post_obj.updated_at.date().isoformat()
                if getattr(post_obj, 'updated_at', None)
                else (post_obj.date.isoformat() if post_obj.date else None)
            ),
        })

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for item in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{item["loc"]}</loc>')
        if item.get('lastmod'):
            xml_parts.append(f'    <lastmod>{item["lastmod"]}</lastmod>')
        xml_parts.append(f'    <changefreq>{item["changefreq"]}</changefreq>')
        xml_parts.append(f'    <priority>{item["priority"]}</priority>')
        xml_parts.append('  </url>')
    xml_parts.append('</urlset>')
    return HttpResponse('\n'.join(xml_parts), content_type='application/xml; charset=utf-8')
