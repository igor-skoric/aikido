from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse
from datetime import time
from django.contrib import messages
from email.utils import formataddr
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Instructor, Blog, Product, Category

import logging
logger = logging.getLogger("django")


def home(request):
    instructors = Instructor.objects.all()[:3]
    context = {'instructors': instructors}
    return render(request, 'website/pages/index.html', context)


def programs(request):
    context = {}
    return render(request, 'website/pages/programs.html', context)


def instructors(request):
    instructors = Instructor.objects.all()[:3]
    context = {'instructors': instructors}
    return render(request, 'website/pages/instructors.html', context)


def instructor(request, slug):
    instructor = Instructor.objects.get(slug=slug)
    context = {'instructor': instructor}
    return render(request, 'website/pages/single_instructor.html', context)


def locations(request):
    context = {}
    return render(request, 'website/pages/locations.html', context)


def blog(request):
    blog = Blog.objects.all()
    context = {'blog': blog}
    return render(request, 'website/pages/blog.html', context)


def post(request, slug):
    post = Blog.objects.get(slug=slug)
    context = {'post': post}
    return render(request, 'website/pages/post.html', context)


def masters(request):
    context = {}
    return render(request, 'website/pages/masters.html', context)


def shop(request):
    category_slug = request.GET.get('category')  # npr. ?category=kimona

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        category = None
        products = Product.objects.all()

    context = {
        'products': products,
        'active_category': category_slug,
        'categories': Category.objects.all(),  # za prikaz filter opcija ako ti zatreba
    }
    return render(request, 'website/pages/shop.html', context)


def product(request, slug):
    product = Product.objects.get(slug=slug)
    related_products = product.get_related_products
    context = {'product': product, 'related_products': related_products}
    return render(request, 'website/pages/single_product.html', context)


def timeline(request):
    context = {}
    return render(request, 'website/pages/timeline.html', context)


def contact(request):
    context = {}
    return render(request, 'website/pages/contact.html', context)