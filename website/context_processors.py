from .models import Config
from django.urls import resolve, reverse


def config(request):
    # Dohvati prvog klijenta sa is_default=True
    config = Config.objects.all().first()
    return {'config': config}


def breadcrumbs(request):
    """Generiše breadcrumbs na osnovu trenutnog URL-a."""
    url_name = resolve(request.path_info).url_name  # Dobijamo ime rute
    kwargs = request.resolver_match.kwargs
    breadcrumbs = [("Početna", "/")]

    if url_name == "timeline":
        breadcrumbs.append(("Istorijat", "/timeline"))
    elif url_name == "contact":
        breadcrumbs.append(("Kontakt", "/contact"))
    elif url_name == "locations":
        breadcrumbs.append(("Lokacije", "/locations"))
    elif url_name == "shop":
        breadcrumbs.append(("Prodavnica", "/shop"))
    elif url_name == "blog":
        breadcrumbs.append(("Blog", "/blog"))
    elif url_name == "programs":
        breadcrumbs.append(("Programi", "/programs"))
    elif url_name == "masters":
        breadcrumbs.append(("Majstori", "/masters"))
    elif url_name == "instructors":
        breadcrumbs.append(("Instruktori", "/instructors"))
    elif url_name == "instructor":
        breadcrumbs.append(("Instruktori", "/instructors"))
        blog_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append((blog_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva
    elif url_name == "product":
        breadcrumbs.append(("Prodavnica", "/shop"))
        blog_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append((blog_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva
    elif url_name == "post":
        breadcrumbs.append(("Blog", "/blog"))
        blog_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append((blog_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva

    return {"breadcrumbs": breadcrumbs}
