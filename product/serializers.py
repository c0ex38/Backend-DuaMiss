from rest_framework import serializers
from .models import Product
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'price', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']

    def validate_name(self, value):
        """Ürün ismi validasyonu"""
        if not value or not value.strip():
            raise serializers.ValidationError("Ürün ismi boş olamaz.")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Ürün ismi en az 2 karakter olmalıdır.")
        
        if len(value) > 255:
            raise serializers.ValidationError("Ürün ismi çok uzun (max 255 karakter).")
        
        return value.strip()

    def validate_code(self, value):
        """Ürün kodu validasyonu"""
        if not value or not value.strip():
            raise serializers.ValidationError("Ürün kodu boş olamaz.")
        
        # Sadece alfanumerik ve bazı özel karakterler
        if not value.replace('-', '').replace('_', '').isalnum():
            raise serializers.ValidationError(
                "Ürün kodu sadece harf, rakam, tire (-) ve alt çizgi (_) içerebilir."
            )
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Ürün kodu en az 2 karakter olmalıdır.")
        
        if len(value) > 50:
            raise serializers.ValidationError("Ürün kodu çok uzun (max 50 karakter).")
        
        # Benzersizlik kontrolü (tüm sistemde unique)
        existing = Product.objects.filter(code__iexact=value.strip())
        
        # Update işleminde mevcut kaydı hariç tut
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise serializers.ValidationError("Bu ürün kodu zaten kullanılıyor.")
        
        return value.strip().upper()  # Kodları büyük harfe çevir

    def validate_price(self, value):
        """Fiyat validasyonu"""
        if value is None:
            raise serializers.ValidationError("Fiyat belirtilmelidir.")
        
        if value < Decimal('0.01'):
            raise serializers.ValidationError("Fiyat 0.01'den küçük olamaz.")
        
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Fiyat çok yüksek (max 999,999.99).")
        
        # 2 ondalık basamak kontrolü
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Fiyat en fazla 2 ondalık basamak içerebilir.")
        
        return value
