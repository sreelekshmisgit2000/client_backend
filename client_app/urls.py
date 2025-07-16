from django.urls import path
from .views import DoctorListCreateView, DoctorDetailView, AllDoctorsView

urlpatterns = [
    #  List & Create doctors
    path('api/doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),

    # Doctor detail by slug
    path('api/doctors/<slug:slug>/', DoctorDetailView.as_view(), name='doctor-detail'),

    #  Count + Full list of doctors (optional separate endpoint)
    path('api/doctors/total/', AllDoctorsView.as_view(), name='doctor-total-list'),
]
