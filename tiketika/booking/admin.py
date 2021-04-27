from django.contrib import admin
from .models import Bus, Booking, Route, Passenger, Faq, Review, Contact
# Register your models here.

admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Route)
admin.site.register(Passenger)
admin.site.register(Faq)
admin.site.register(Review)
admin.site.register(Contact)