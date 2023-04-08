from django.db import models
from user.models import UserModel
class ProductModel(models.Model):
    class Meta:
        db_table = "product_register"
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=30, unique=True) #코드 번호
    name = models.CharField(max_length=50) #상품 이름 
    category = models.CharField(max_length=30) #상품 카테고리, 종류
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'XLarge'),
        ('F', 'Free')
    )
    size = models.CharField(choices=sizes, max_length=2) #상품 사이즈
    #choices매개변수는 해당 필드에서 선택 가능한 옵션을 지정하는 역할
    #변수를 통해 튜플리스트를 받으면 1번째 요소는 DB에 저장되고, 2번째 요소는 사용자가 볼 수 있는 레이블이 된다.
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Inbound(models.Model):
    """
    입고 모델
    상품, 수량, 입고 날짜, 금액 
    """
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Outbound(models.Model):
    """
    출고 모델
    상품, 수량, 입고 날짜, 금액
    """
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Inventory(models.Model):
    """
    창고 제품과 수량 정보를 담는 모델
    상품, 수량
    OneToOne 관계 작성
    """
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
