from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from blog.models import Article, BlogCategory
from courses.models import Course, CourseCategory
from products.models import Category, Product
from rentals.models import RentalItem
from website.models import Banner, Service, Testimonial


class Command(BaseCommand):
    help = "Cree des donnees de demonstration BKLN-TECH."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@bkln-tech.com", "is_staff": True, "is_superuser": True})
        admin.set_password("admin12345")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        Banner.objects.get_or_create(
            title="BKLN-TECH",
            defaults={"subtitle": "Votre partenaire numerique de confiance."},
        )
        services = [
            ("Developpement web", "Sites, plateformes, API REST et tableaux de bord professionnels."),
            ("Maintenance informatique", "Reparation, installation Windows/Linux, antivirus et reseaux."),
            ("Intelligence artificielle", "Automatisation, IA generative, NLP et vision par ordinateur."),
            ("Administration numerique", "Legalisation, QR Code, verification publique et dossiers en ligne."),
        ]
        for title, summary in services:
            Service.objects.get_or_create(slug=title.lower().replace(" ", "-"), defaults={"title": title, "summary": summary})
        Testimonial.objects.get_or_create(author="Client institutionnel", defaults={"position": "Bangui", "message": "Une equipe fiable, rapide et tres professionnelle."})

        for name, slug in [("Ordinateurs", "ordinateurs"), ("Imprimantes", "imprimantes"), ("Accessoires informatiques", "accessoires"), ("Logiciels et antivirus", "logiciels-antivirus"), ("Maintenance informatique", "maintenance-informatique")]:
            Category.objects.get_or_create(slug=slug, defaults={"name": name})
        category = Category.objects.get(slug="ordinateurs")
        Product.objects.get_or_create(
            slug="ordinateur-portable-pro",
            defaults={"category": category, "name": "Ordinateur portable Pro", "sku": "BKLN-PC-001", "description": "Portable professionnel pour bureau, formation et developpement.", "price": 450000, "stock": 12, "featured": True, "image": "shop/products/hp-elitebook-1050.png"},
        )
        demo_products = [
            ("HP EliteBook 850", "hp-elitebook-850", "BKLN-PC-850", "ordinateur portable HP EliteBook 850 robuste.", 280000, "shop/products/hp-elitebook-850.webp", "ordinateurs"),
            ("Clavier HP de remplacement", "clavier-hp-remplacement", "BKLN-ACC-KB", "Clavier compatible ordinateurs portables HP.", 25000, "shop/products/hp-keyboard.webp", "accessoires"),
            ("Kaspersky Standard", "kaspersky-standard", "BKLN-AV-KAS", "Licence antivirus Kaspersky Standard.", 30000, "shop/products/kaspersky-standard-box.webp", "logiciels-antivirus"),
            ("Maintenance ordinateur", "maintenance-ordinateur", "BKLN-SVC-MAINT", "Diagnostic, nettoyage et reparation ordinateur.", 20000, "shop/products/maintenance-technician.webp", "maintenance-informatique"),
        ]
        for name, slug, sku, description, price, image, category_slug in demo_products:
            Product.objects.get_or_create(
                slug=slug,
                defaults={"category": Category.objects.get(slug=category_slug), "name": name, "sku": sku, "description": description, "price": price, "stock": 10, "featured": True, "image": image},
            )

        parent, _ = CourseCategory.objects.get_or_create(slug="developpement-web", defaults={"name": "Developpement Web"})
        Course.objects.get_or_create(
            slug="formation-developpement-web",
            defaults={
                "category": parent,
                "trainer": admin,
                "title": "Formation Developpement Web",
                "description": "Introduction aux bonnes pratiques du developpement web, conception de sites et creation de projets en equipe.",
                "price": 45000,
                "published": True,
            },
        )
        blog_category, _ = BlogCategory.objects.get_or_create(slug="actualites", defaults={"name": "Actualites"})
        Article.objects.get_or_create(
            slug="transformation-numerique-centrafrique",
            defaults={"category": blog_category, "author": admin, "title": "Transformation numerique en Centrafrique", "excerpt": "Les opportunites du numerique pour les entreprises et administrations.", "content": "BKLN-TECH accompagne la transition numerique avec des outils modernes.", "published": True},
        )
        RentalItem.objects.get_or_create(name="Videoprojecteur HD", defaults={"category": "Presentation", "description": "Materiel disponible pour seminaires et formations.", "daily_price": 15000, "deposit": 50000})
        self.stdout.write(self.style.SUCCESS("Donnees de demonstration creees. Superutilisateur: admin / admin12345"))
