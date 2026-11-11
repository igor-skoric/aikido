from django.urls import resolve

from .models import Config


def config(request):
    return {'config': Config.get_solo()}


def breadcrumbs(request):
    url_name = resolve(request.path_info).url_name
    kwargs = request.resolver_match.kwargs
    crumbs = [('Početna', '/')]

    mapping = {
        'timeline': ('Istorijat', '/timeline/'),
        'contact': ('Kontakt', '/contact/'),
        'locations': ('Lokacije', '/locations/'),
        'blog': ('Blog', '/blog/'),
        'programs': ('Programi', '/programs/'),
        'masters': ('Majstori', '/masters/'),
        'instructors': ('Instruktori', '/instructors/'),
    }

    if url_name in mapping:
        crumbs.append(mapping[url_name])
    elif url_name == 'instructor':
        crumbs.append(('Instruktori', '/instructors/'))
        slug = kwargs.get('slug', '')
        crumbs.append((slug.replace('-', ' ').title(), request.path))
    elif url_name == 'post':
        crumbs.append(('Blog', '/blog/'))
        slug = kwargs.get('slug', '')
        crumbs.append((slug.replace('-', ' ').title(), request.path))

    return {'breadcrumbs': crumbs}
