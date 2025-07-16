from rest_framework import serializers
from .models import Webinar,WebinarBooking
from django.utils import timezone


class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = '__all__'

    # 🔹 Validate: Date must be future or today
    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Webinar date must be in the future.")
        return value

    # 🔹 Validate: Registration deadline must be before the date
    def validate_registration_deadline(self, value):
        date = self.initial_data.get('date')
        if value and date and value >= timezone.datetime.fromisoformat(date):
            raise serializers.ValidationError("Registration deadline must be before webinar date.")
        return value

    # 🔹 Price validation
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value



class WebinarBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarBooking
        fields = [
            'id',
            'user',
            'webinar',
            'razorpay_order_id',
            'razorpay_payment_id',
            'razorpay_signature',
            'is_paid',
            'created_at'
        ]
        read_only_fields = ['razorpay_payment_id', 'razorpay_signature', 'is_paid', 'created_at']