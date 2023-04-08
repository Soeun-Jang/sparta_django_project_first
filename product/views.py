from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductModel, Inbound, Outbound # 글쓰기 모델
from django.db import transaction
from django.db import IntegrityError



#====사용자 인증 여부에 따라 홈페이지 또는 트윗 페이지로 이동하는 코드====
def home(request):
    user = request.user.is_authenticated  
    # 사용자가 인증을 받았는지 (로그인이 되어있는지)
    if user:
        return redirect('/product')
    else:
        return redirect('/signin')

#=======등록된 상품 리스트를 볼 수 있는 view========
@login_required
def product_list(request):
    if request.method == 'GET': #GET메소드로 요청 들어 올 경우
        all_product = ProductModel.objects.all().order_by('-created_at') #등록 역순으로 불러오기 
        return render(request, 'product/product_list.html', {'allproduct': all_product}) 

#==============상품 등록 view==============
@login_required
def product_create(request):
    if request.method == 'GET': #GET메소드로 요청 들어 올 경우
        return render(request, 'product/product_create.html')
    if request.method == 'POST':  # 요청 방식이 POST 일때
        user = request.user  # 현재 로그인 한 사용자를 불러오기
        my_product = ProductModel()  # 상품 등록 모델 가져오기
        my_product.author = user  # 모델에 사용자 저장
        
        #각 데이터모델 필드에 입력 받은 값 저장
        my_product.code =  request.POST.get('code', '') 
        my_product.description = request.POST.get('mydescription', '') 
        my_product.name =  request.POST.get('name', '')
        my_product.category =  request.POST.get('category', '')
        my_product.price =  int(request.POST.get('price', '0'))
        my_product. size =  request.POST.get('size', '')
        try:
            my_product.save()
            return redirect('/product') 
        except IntegrityError:
            error_message_code = f"코드 번호 '{my_product.code}'는 이미 등록되어 있습니다."
            return render(request, 'product/product_create.html', {'error_message_code': error_message_code})
    else:
        return redirect('/product')

        # if not all(my_product.__dict__.values()):
        #     error_message = "입력값이 없습니다."
        #     return render(request, 'product/product_create.html', {'error_message': error_message})
        
#=======상품 입고 view============
@login_required
@transaction.atomic 
def inbound_create(request):
    if request.method == 'GET':
        all_inbound = Inbound.objects.all().order_by('-id') #id역순으로 불러오기 
        #ProductModel에서 code필드 값 가져오기
        #value_list() : 쿼리셋에서 특정 필드 값 가져올 때
        #'flat=True' : 해당 필드 값들을 리스트가 아닌 단순 값들의 이터레이터로 반환 
        product_codes = ProductModel.objects.values_list('code', flat=True) 
        return render(request, 'product/inbound_create.html', {'allinbound': all_inbound, 'code': product_codes} )
    if request.method == 'POST':
        code = request.POST.get('code','')
        quantity = int(request.POST.get('quantity', 0))
        #filter() : 지정된 필드 값과 일치하는 객체 검색, filter(필드 값 = 검색할 코드 값)
        products = ProductModel.objects.filter(code=code) 
        if products.exists():
            # 제품이 이미 등록되어 있는 경우
            # 여러 개의 제품 중 어떤 것을 선택할 것인지 지정
            product = products.first()  # 첫 번째 제품 선택
            product.stock += quantity #ProductModel 객체의 stock에 입력받은 수량 저장
            product.save() 
            amount = quantity * product.price #가격 = 수량 * 제품 금액 
            inbound = Inbound(quantity=quantity, product=product, amount=amount)
            inbound.save()
        else:
            # 제품이 등록되어 있지 않은 경우
            product = ProductModel(code=code, stock=quantity)
            product.save()
            amount = quantity * product.price
            inbound = Inbound(quantity=quantity, product=product, amount=amount)
            inbound.save()
    return redirect('/product/inbound')


#==============상품 출고 view================
@login_required
def outbound_create(request):
    if request.method == 'GET':
        all_outbound = Outbound.objects.all().order_by('-id')
        product_codes = ProductModel.objects.all().values_list('code', flat=True)
        return render(request, 'product/outbound_create.html', {'alloutbound': all_outbound, 'code': product_codes})
    if request.method == 'POST':
        code = request.POST.get('code','')
        quantity = int(request.POST.get('quantity', 0))
        try: #입력된 code값으로 ProductModel에서 해당 제품 가져오기 
            product = ProductModel.objects.get(code=code) 
        except ProductModel.DoesNotExist:  #일치 제품이 없는 경우 예외처리 
            print('error')
            return redirect('/product')
        if product.stock < quantity:
            # 재고 수량이 출고 수량보다 작은 경우
            # 해당 제품 출고 불가능
            all_outbound = Outbound.objects.all().order_by('-id')
            product_codes = ProductModel.objects.all().values_list('code', flat=True)
            return render(request, 'product/outbound_create.html', {'alloutbound': all_outbound, 'code': product_codes, 'message':'재고 수량이 출고 수량보다 작습니다.'})
        product.stock -= quantity
        amount = quantity * product.price
        outbound = Outbound(quantity=quantity, product=product,amount=amount)
        product.save()
        outbound.save() 
    
        return redirect('/product/outbound')


#=========재고 현황 view===============
@login_required
def inventory(request):
    #Inbound, Outbound 모델의 모든 데이터 가져오기
    #select_related메소드 이용 -> 외래키 관계인 Product의 모델 데이터도 함께 가져오기
    inbounds = Inbound.objects.all().select_related('product')
    outbounds = Outbound.objects.all().select_related('product')
    
    #입고 정산 
    total_inbound_quantity = sum(inbound.quantity for inbound in inbounds)
    total_inbound_amount = sum(inbound.quantity * inbound.product.price for inbound in inbounds)
    #출고 정산
    total_outbound_quantity = sum(outbound.quantity for outbound in outbounds)
    total_outbound_amount = sum(outbound.quantity * outbound.product.price for outbound in outbounds)
    #계산 값들 딕셔너리 형태로 변수 context에 저장
    context = {
        'total_inbound_quantity': total_inbound_quantity,
        'total_inbound_amount': total_inbound_amount,
        'total_outbound_quantity': total_outbound_quantity,
        'total_outbound_amount': total_outbound_amount,
    }
    #렌더링하면서 context 값 함께 전달 
    return render(request, 'product/inventory.html', context)

    """
    inbound_create, outbound_create 뷰에서 만들어진 데이터 합산
    django ORM을 통하여 수량, 가격 계산,.. 
    
    총 입고 수량 ,가격 계산
    총 출고 수량, 가격 계산
    """

#=========제품 검색 view ============
def proudct_search(request):
    if request.method == 'GET':
        return render(request, 'product/product_search.html')
    if request.method == 'POST':
        search_code = request.POST.get('search_code', '') # 검색어 추출 
        #DB에서 일치하는 제품 가져오기
        products = ProductModel.objects.filter (code=search_code) 
        return render(request, 'product/product_search.html', {'products': products})
    else:
        return redirect('/product')