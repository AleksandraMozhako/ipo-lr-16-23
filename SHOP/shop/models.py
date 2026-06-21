from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Manufacturer(models.Model):
    """Производитель товаров для пикника"""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория товаров (корзины, пледы, посуда)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар для пикника"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="products"
    )
    
    def clean(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        if self.stock_quantity < 0:
            raise ValidationError("Количество на складе не может быть отрицательным")
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    """Корзина покупателя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    
    def clean(self):
        if self.quantity > self.product.stock_quantity:
            raise ValidationError(
                f"Доступно только {self.product.stock_quantity} товаров на складе"
            )
    
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"
    
class Order(models.Model):
    """Заказ покупателя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    email = models.EmailField()
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"


class OrderItem(models.Model):
    """Позиция заказа"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.product_name} ({self.quantity} шт.)"
