from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Banner(TimeStampedModel):
    title = models.CharField(max_length=180)
    subtitle = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banners/", blank=True)
    cta_label = models.CharField(max_length=80, default="Demander un devis")
    cta_url = models.CharField(max_length=160, default="/devis/")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Service(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=60, default="cpu")
    summary = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    author = models.CharField(max_length=160)
    position = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.author


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject


class QuoteRequest(TimeStampedModel):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    service = models.CharField(max_length=160)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    details = models.TextField()
    status = models.CharField(max_length=30, default="new")

    def __str__(self):
        return f"Devis - {self.name}"


class NewsletterSubscriber(TimeStampedModel):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

# Create your models here.
