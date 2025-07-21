from django.shortcuts import render
from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer

# Create your views here.

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')
