from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    referrals = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'referred_by', 'referrals']
