from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('route_list/', views.route_list, name='route_list'),
    path('booking_info/<int:pk>', views.booking_info, name='booking_info'),
    path('booking/', views.booking, name='booking'),
    path('ticket/', views.ticket, name='ticket'),
    path('cancel/', views.cancel, name='cancel'),
    path('asked_question/', views.faq, name='faq'),
    path('review/', views.review, name='review'),
    path('contact/', views.contact, name='contact'),
    path('complete_payment/', views.complete_payment, name='complete_payment'),
    path('success_paid/<int:pk>', views.success_paid, name='success_paid'),
    path('download_ticket/<int:pk>', views.Pdf.as_view(), name='pdf'),
    path('helps/', views.helps, name='helps'),
    path('service/', views.service, name='service'),
]