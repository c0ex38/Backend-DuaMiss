from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def validate_username(self, value):
        """Kullanıcı adı validasyonu"""
        if not value or not value.strip():
            raise serializers.ValidationError("Kullanıcı adı boş olamaz.")
        
        # Minimum 3 karakter
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Kullanıcı adı en az 3 karakter olmalıdır.")
        
        # Maksimum 150 karakter
        if len(value) > 150:
            raise serializers.ValidationError("Kullanıcı adı çok uzun (max 150 karakter).")
        
        # Sadece alfanumerik, alt çizgi ve tire
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise serializers.ValidationError(
                "Kullanıcı adı sadece harf, rakam, alt çizgi (_) ve tire (-) içerebilir."
            )
        
        # Rakamla başlayamaz
        if value[0].isdigit():
            raise serializers.ValidationError("Kullanıcı adı rakamla başlayamaz.")
        
        return value.strip().lower()

    def validate_password(self, value):
        """Şifre validasyonu"""
        if len(value) < 8:
            raise serializers.ValidationError("Şifre en az 8 karakter olmalıdır.")
        
        # En az bir büyük harf
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Şifre en az bir büyük harf içermelidir.")
        
        # En az bir küçük harf
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Şifre en az bir küçük harf içermelidir.")
        
        # En az bir rakam
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Şifre en az bir rakam içermelidir.")
        
        # En az bir özel karakter
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Şifre en az bir özel karakter içermelidir (!@#$%^&* vb.).")
        
        return value

    def validate(self, attrs):
        """Şifre eşleşme kontrolü"""
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        
        # Eğer password_confirm gönderildiyse kontrol et
        if password_confirm and password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': 'Şifreler eşleşmiyor.'
            })
        
        return attrs

    def create(self, validated_data):
        # password_confirm'i çıkar (modelde yok)
        validated_data.pop('password_confirm', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
