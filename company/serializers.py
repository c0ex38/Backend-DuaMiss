from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']

    def validate_name(self, value):
        """Şirket ismi validasyonu"""
        # Boş veya sadece boşluk kontrolü
        if not value or not value.strip():
            raise serializers.ValidationError("Şirket ismi boş olamaz.")
        
        # Minimum uzunluk kontrolü
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Şirket ismi en az 2 karakter olmalıdır.")
        
        # Maximum uzunluk kontrolü (model'de 255)
        if len(value) > 255:
            raise serializers.ValidationError("Şirket ismi çok uzun (max 255 karakter).")
        
        # Aynı kullanıcının aynı isimle başka şirket olup olmadığı
        user = self.context['request'].user
        existing = Company.objects.filter(
            owner=user,
            name__iexact=value.strip()
        )
        
        # Update işleminde mevcut kaydı hariç tut
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise serializers.ValidationError("Bu isimde bir şirket zaten kayıtlı.")
        
        return value.strip()
