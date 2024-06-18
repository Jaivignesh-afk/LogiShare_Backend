from rest_framework import serializers
from .models import Customer, Shipment

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    # Confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Customer
        fields = ('email','name', 'phone_number', 'password')

    def validate(self, data):
        # if data['password'] != data['Confirm_password']:
        #     raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # validated_data.pop('Confirm_password')
        user = Customer.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    # email = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

# class ShipmentPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shipment
#         fields = ['Type', 'Q', 'Width', 'Weight', 'Height', 'Quantity', 'Pickup', 'Drop', 'customer', 'p_pincode', 'd_pincode']

# class ShipmentUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shipment
#         fields = ['photo']