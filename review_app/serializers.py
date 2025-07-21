from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'client_name', 'review_text', 'rating', 'image', 'created_at', 'diagnosis']
        read_only_fields = ['created_at', 'id']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def validate_image(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError('Image size should not exceed 2MB.')
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError('Uploaded file must be an image.')
        return value
