from django.contrib import admin

from .models import Banner, ContactMessage, NewsletterSubscriber, QuoteRequest, Service, Testimonial

admin.site.register(Banner)
admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
admin.site.register(QuoteRequest)
admin.site.register(NewsletterSubscriber)

# Register your models here.
