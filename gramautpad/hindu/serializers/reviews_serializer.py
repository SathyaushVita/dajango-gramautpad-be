from rest_framework import serializers
from ..models import Review,User

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Review
        fields = ['_id', 'review_text', 'rating', 'product', 'user', 'created_at']
        read_only_fields = ['_id', 'created_at']

    def validate_rating(self, value):
        """Ensure the rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
