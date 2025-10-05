from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from company.models import Company
from decimal import Decimal
from django.shortcuts import get_object_or_404


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_code = serializers.ReadOnlyField(source='product.code')

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_code',
            'quantity', 'unit_price', 'item_discount'
        ]

    def validate_quantity(self, value):
        """Miktar validasyonu"""
        if value < 1:
            raise serializers.ValidationError("Miktar en az 1 olmalıdır.")
        if value > 999999:
            raise serializers.ValidationError("Miktar çok yüksek (max 999,999).")
        return value

    def validate_unit_price(self, value):
        """Birim fiyat validasyonu"""
        if value < Decimal('0.01'):
            raise serializers.ValidationError("Birim fiyat 0.01'den küçük olamaz.")
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Birim fiyat çok yüksek (max 999,999.99).")
        return value

    def validate_item_discount(self, value):
        """Ürün indirimi validasyonu"""
        if value < 0:
            raise serializers.ValidationError("İndirim oranı negatif olamaz.")
        if value > 100:
            raise serializers.ValidationError("İndirim oranı 100'den büyük olamaz.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Order
        fields = [
            'id', 'company', 'company_name', 'delivery_date', 'created_at', 'owner',
            'global_discount', 'vat_rate',
            'subtotal', 'discount_amount', 'vat_amount', 'total',
            'items'
        ]
        read_only_fields = [
            'id', 'created_at', 'owner',
            'subtotal', 'discount_amount', 'vat_amount', 'total'
        ]

    def validate_company(self, value):
        """Şirketin kullanıcıya ait olduğunu kontrol et"""
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("Bu şirket size ait değil.")
        return value

    def validate_global_discount(self, value):
        """Global indirim oranı validasyonu"""
        if value < 0:
            raise serializers.ValidationError("İndirim oranı negatif olamaz.")
        if value > 100:
            raise serializers.ValidationError("İndirim oranı 100'den büyük olamaz.")
        return value

    def validate_vat_rate(self, value):
        """KDV oranı validasyonu"""
        if value < 0:
            raise serializers.ValidationError("KDV oranı negatif olamaz.")
        if value > 100:
            raise serializers.ValidationError("KDV oranı 100'den büyük olamaz.")
        return value

    def validate_items(self, items_data):
        """Ürünlerin kullanıcıya ait olduğunu ve geçerli olduğunu kontrol et"""
        if not items_data:
            raise serializers.ValidationError("Sipariş en az bir ürün içermelidir.")
        
        user = self.context['request'].user
        
        for idx, item in enumerate(items_data, 1):
            product = item.get('product')
            
            # Ürün kontrolü
            if not product:
                raise serializers.ValidationError(f"Ürün {idx}: Ürün belirtilmemiş.")
            
            # Ürün sahipliği kontrolü
            if product.owner != user:
                raise serializers.ValidationError(
                    f"Ürün '{product.name}' size ait değil."
                )
            
            # Miktar kontrolü
            quantity = item.get('quantity')
            if not quantity or quantity < 1:
                raise serializers.ValidationError(
                    f"Ürün '{product.name}': Miktar en az 1 olmalıdır."
                )
            if quantity > 999999:
                raise serializers.ValidationError(
                    f"Ürün '{product.name}': Miktar çok yüksek (max 999,999)."
                )
            
            # Birim fiyat kontrolü
            unit_price = item.get('unit_price')
            if unit_price is None or unit_price < Decimal('0.01'):
                raise serializers.ValidationError(
                    f"Ürün '{product.name}': Birim fiyat 0.01'den küçük olamaz."
                )
            if unit_price > Decimal('999999.99'):
                raise serializers.ValidationError(
                    f"Ürün '{product.name}': Birim fiyat çok yüksek."
                )
            
            # Ürün indirimi kontrolü
            item_discount = item.get('item_discount', Decimal('0'))
            if item_discount < 0:
                raise serializers.ValidationError(
                    f"Ürün '{product.name}': İndirim oranı negatif olamaz."
                )
            if item_discount > 100:
                raise serializers.ValidationError(
                    f"Ürün '{product.name}': İndirim oranı 100'den büyük olamaz."
                )
        
        return items_data

    def _calculate_totals(self, order, items_data):
        """Sipariş toplamlarını hesapla"""
        subtotal = Decimal('0')

        # Ürün bazlı hesaplama
        for item_data in items_data:
            quantity = item_data['quantity']
            price = item_data['unit_price']
            discount = item_data.get('item_discount', Decimal('0'))

            # Ürün bazlı indirim hesapla
            discounted_price = price - (price * discount / 100)
            subtotal += discounted_price * quantity

        # Genel iskonto ve KDV
        general_discount = order.global_discount
        discount_amount = subtotal * general_discount / 100
        discounted_total = subtotal - discount_amount
        vat_amount = discounted_total * order.vat_rate / 100
        total = discounted_total + vat_amount

        # Değerleri güncelle
        order.subtotal = subtotal
        order.discount_amount = discount_amount
        order.vat_amount = vat_amount
        order.total = total
        order.save()

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        validated_data.pop('owner', None)
        order = Order.objects.create(owner=user, **validated_data)

        # Ürünleri kaydet
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        # Toplamları hesapla
        self._calculate_totals(order, items_data)

        return order

    def update(self, instance, validated_data):
        """Sipariş güncelleme"""
        items_data = validated_data.pop('items', None)
        
        # Order alanlarını güncelle
        instance.company = validated_data.get('company', instance.company)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.global_discount = validated_data.get('global_discount', instance.global_discount)
        instance.vat_rate = validated_data.get('vat_rate', instance.vat_rate)
        instance.save()

        # Eğer items güncellenmişse
        if items_data is not None:
            # Eski itemları sil
            instance.items.all().delete()
            
            # Yeni itemları ekle
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
            
            # Toplamları yeniden hesapla
            self._calculate_totals(instance, items_data)
        
        return instance
