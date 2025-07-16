from django.urls import path
from .views import WebinarListView, WebinarDetailView,create_webinar_booking,razorpay_webhook,register_user

urlpatterns = [
    path('api/webinars/', WebinarListView.as_view(), name='webinar-list'),
    path('api/webinars/<slug:slug>/', WebinarDetailView.as_view(), name='webinar-detail'),
    path('book-webinar/<int:webinar_id>/', create_webinar_booking, name='create_webinar_booking'),
    path('payment/webhook/', razorpay_webhook, name='razorpay_webhook'),
    path('register/', register_user, name='register_user'),
]
