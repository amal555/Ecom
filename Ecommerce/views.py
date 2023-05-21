from django.shortcuts import render
from django.http import JsonResponse
from .models import Customers,Productss,User
from django.contrib.auth.models import auth
import json
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
def home(request):
    return render(request,'login.html')

def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        username = data["username"]
        name = data["name"]
        email = data["email"]
        password = data["password"]
        try:
            Customers.objects.create_user(username=username, name=name, email=email,password=password)
        except Exception as e:
            return JsonResponse({"msg":"Something went worng.Please try again"})
        return JsonResponse({"msg":"Succssfully created Please Login","status":200})
    else:
        return JsonResponse({"msg":"Method not allowed"})
    
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        username = data["username"]
        password = data["password"]
        try:
            customer_obj = Customers.objects.filter(username=username)
            if customer_obj:
                request.session['user_id'] = customer_obj.first().id
                return JsonResponse({"status":200})
            else:
                return JsonResponse({"status":500,"msg":"No User Found"})
        except Exception as e:
            return JsonResponse({"status":500,"msg":"Something went wrong.Please try again"})
    else:
        return JsonResponse({"msg":"Method not allowed"})
    
def homepage(request):
    return render(request,'home.html')

def add_products(request):
    return render(request,'add_products.html')

def add_product_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        data['customers_id'] = request.session['user_id']
        
        try:
            user_obj = User.objects.get(id=data['id'])
            Productss.objects.update_or_create(
                customers_id=data['customers_id'],
                products_user=user_obj,
                products_name=data['products_name'],
                image_data=data['image_data'],
                description=data['description'],
                price=data['price'],
                discount=data['discount']
            )
            return JsonResponse({'msg': 'Successfully added products',"status":200})
        except Exception as e:
            print(e)
            return JsonResponse({'msg': f'Failed to add. Please try again{e}'})
    else:
        return JsonResponse({'msg': 'Method not allowed'})
    
def dashboard(request):
    id = request.session['user_id']
    try:
        prod_obj = Productss.objects.filter(customers_id=id).select_related('customers')
        if prod_obj:
            context = {'name': prod_obj.first().customers.name,
                    'email': prod_obj.first().customers.email,
                    'username': prod_obj.first().customers.username
                    }
        else:
            customer_obj = Customers.objects.filter(id=id)
            context = {'name': customer_obj.first().name,
                    'email': customer_obj.first().email,
                    'username': customer_obj.first().username
                    }
    except Exception as e:
        context = {}
    return render(request,'dashboard.html',{"data":context})
    
from rest_framework import serializers  
class ProductSerializer(serializers.ModelSerializer):
    # Define any additional fields or related serializers as needed
    products_user = serializers.CharField(source="products_user.customer_name")

    class Meta:
        model = Productss
        fields = "__all__"
    

class ProductTable(APIView):
    COLUMN_ORDER = [
        "-created_date", 
        "products_user",
        "products_name",
        "price",
        "description",
        "discount",
        "image_data",
        "created_date",
        "is_active",
        "is_active",
    ]
    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get("search[value]")
        if search_query:
            queryset = queryset.annotate(search=SearchVector("name")).filter(
                search=search_query
            )
        params = self.request.query_params.dict()
        order_column = params.get("order[0][column]")
        order = params.get("order[0][dir]")

        keys_to_remove = [
            "draw",
            "order[0][column]",
            "order[0][dir]",
            "start",
            "length",
            "search[value]",
            "search[regex]",
            "_",
            "type",
            "excel",
        ]
        for key in keys_to_remove:
            params.pop(key, None)
        obj_dict = {k: v for k, v in params.items() if v}
        if order_column:
            order_column = int(order_column[0])
            order_column = self.COLUMN_ORDER[order_column]
            if order == "desc":
                order_column = "-" + order_column
            if obj_dict:
                queryset = queryset.filter(**obj_dict)
            queryset = queryset.order_by(order_column)
        else:
            queryset = queryset.filter(**obj_dict)
        return queryset

    def get(self, request, *args, **kwargs):
        draw = request.query_params.get("draw")
        start = int(request.query_params.get("start", 0))
        length = int(request.query_params.get("length", 5))
        end = length + start
        queryset = Productss.objects.filter()
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        serializer = ProductSerializer(filtered_queryset[start:end], many=True)
        response = {
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": filtered_queryset.count(),
            "data": serializer.data,
        }
        return Response(response)

def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        id = request.session['user_id']
        try:
            Productss.objects.filter(customers_id=id,products_name=data['products_name']).update(is_active=data['is_active'])
            return JsonResponse({"msg": "successfully changed status", "status":200})
        except Exception as e:
            return JsonResponse({"msg": "updation failed", "status":500})
    else:
        return JsonResponse({"msg":"Method not allowed"})
    
def customers_dashboard(request):
    id = request.session['user_id']
    try:
        customer_obj  = User.objects.select_related('customers_user', 'products_user').all()
        if customer_obj:
            context = {'name': customer_obj.first().customer_name,
                    'customers_address': customer_obj.first().customers_address,
                    'mobile_number': customer_obj.first().mobile_number
                    }
        else:
            customer_obj = User.objects.filter(id=id)
            context = {'name': customer_obj.first().customer_name,
                    'customers_address': customer_obj.first().customers_address,
                    'mobile_number': customer_obj.first().mobile_number
                    }
    except Exception as e:
        context = {}
    return render(request,'customer_page.html',context)

class CustomerTable(APIView):
    COLUMN_ORDER = [
        "-created_date", 
        "customer_name",
        "customers_address",
        "mobile_number",
    ]
    def filter_for_datatable(self, queryset):
        search_query = self.request.query_params.get("search[value]")
        if search_query:
            queryset = queryset.annotate(search=SearchVector("name")).filter(
                search=search_query
            )
        params = self.request.query_params.dict()
        order_column = params.get("order[0][column]")
        order = params.get("order[0][dir]")

        keys_to_remove = [
            "draw",
            "order[0][column]",
            "order[0][dir]",
            "start",
            "length",
            "search[value]",
            "search[regex]",
            "_",
            "type",
            "excel",
        ]
        for key in keys_to_remove:
            params.pop(key, None)
        obj_dict = {k: v for k, v in params.items() if v}
        if order_column:
            order_column = int(order_column[0])
            order_column = self.COLUMN_ORDER[order_column]
            if order == "desc":
                order_column = "-" + order_column
            if obj_dict:
                queryset = queryset.filter(**obj_dict)
            queryset = queryset.order_by(order_column)
        else:
            queryset = queryset.filter(**obj_dict)
        return queryset

    def get(self, request, *args, **kwargs):
        draw = request.query_params.get("draw")
        start = int(request.query_params.get("start", 0))
        length = int(request.query_params.get("length", 5))
        end = length + start
        queryset = User.objects.filter()
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        response = {
            "draw": draw,
            "recordsTotal": recordsTotal,
            "recordsFiltered": filtered_queryset.count(),
            "data": list(filtered_queryset[start:end].values()),
        }
        return Response(response)
    
def add_customer_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        customer_obj = Customers.objects.get(id=request.session['user_id'])
        data["customers_user"] = customer_obj
        try:
            User.objects.update_or_create(**data)
        except Exception as e:
            print(e)
            return JsonResponse({'msg': 'Failed to add.Please try again'})
        return JsonResponse({'msg': 'Successfully added customer'})
    else:
        return JsonResponse({'msg': 'method not allowed'})
    
def add_customers(request):
    return render(request,'add_customers.html')

def delete_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        User.objects.filter(id=data["id"]).delete()
        return JsonResponse({'msg': 'Successfully deleted customer'})
    else:
        return JsonResponse({'msg': 'method not allowed'})
    
def edit_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        try:
            user_obj = User.objects.filter(id=data["id"]).first()
            context = {'customer_name': user_obj.customer_name,
                       'customers_address':user_obj.customers_address,
                       'mobile_number':user_obj.mobile_number}
            return JsonResponse({'data': context,"status":200})
        except Exception as e:
            print(e)
            return JsonResponse({"status":500,"msg":"Something went wrong.Please try again"})
    else:
        return JsonResponse({'msg': 'method not allowed'})

def update_customer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("UTF-8"))
        try:
            User.objects.filter(id=data["id"]).update(**data)
            return JsonResponse({'msg': "Successfully updated","status":200})
        except Exception as e:
            print(e)
            return JsonResponse({"status":500,"msg":"Something went wrong.Please try again"})
    else:
        return JsonResponse({'msg': 'method not allowed'})