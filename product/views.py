import json
from django.http import JsonResponse
from .models import Shipment, Transporter, Customer, Quotes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import os
from myproject import settings
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ShipmentSerializer
from rest_framework.views import APIView
from django.utils.decorators import method_decorator




@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data.get('name'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def post(self, request): 
        # email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        print(os.path.join(settings.MEDIA_URL, 'shipment_photos', '16624708281241124901334187442120.jpg'))
        cust_user = authenticate(phone_number=phone_number,password=password)
        trans_user = None
        try:
            trans_user = Transporter.objects.get(phone = phone_number, password_hash = password)
        except Exception as e:
            print(e)
        if cust_user is not None:
            # Additional actions upon successful login (if needed)
            return Response({'message': 'Customer Login Successfull', 'user_id' : str(cust_user.pk), 'is_customer': True}, status=status.HTTP_200_OK)
        elif trans_user is not None:

            return Response({'message': 'Transporter Login Successfull', 'user_id': str(trans_user.pk), 'is_customer': False}, status = status.HTTP_200_OK)
        # else:
        #         # Inactive user account
        #         return Response({'message': 'User account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Invalid credentials
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
# def home(request):
#     mydata=Shipment.objects.all()
#     if(mydata!=''):
#         return render(request,'home.html', {'datas':mydata})
#     else:
#         return render(request,'home.html')


@csrf_exempt
def sendListing(request, id):
    if request.method == 'GET':
        return JsonResponse({'shipmentID': str(id),
                            'pickupLocation' : Shipment.objects.get(id=id).Pickup,
                            'deliveryLocation':Shipment.objects.get(id=id).Drop,
                            'shipmentWeight':str(Shipment.objects.get(id=id).Weight),
                            'itemName':Shipment.objects.get(id=id).Type,
                            'photo': Shipment.objects.get(id=id).photo.name,
                            'category':  Shipment.objects.get(id=id).category }, status=200,)

@csrf_exempt    
def store_quote(request):
    if request.method == "POST":
        data = json.loads(request.body)
        shipmentId = int(data.get("ship_id"))
        transporterId = int(data.get("trans_id"))
        quote = int(data.get("quote"))
        q = Quotes()
        q.quote = quote
        q.transporter = Transporter.objects.get(id = transporterId)
        ship = Shipment.objects.get(id = shipmentId)
        ship.quotes = q
        q.shipment = ship
        q.save()
        ship.save()
        return JsonResponse({'message': "working"}, status = status.HTTP_200_OK)

@csrf_exempt
def displayshipments(request, id):
    if request.method == "GET":
        shipments = Shipment.objects.filter(customer = Customer.objects.get(id = id))
        data = list(shipments.values())
        send = []
        for d in data:
            if not d["is_accepted"]:
                send.append(d)
        return JsonResponse({'data': send }, status=200)
    
@csrf_exempt
def translisting(request):
    if request.method == "GET":
        
        trans_id = request.GET.get('transid')
        shipment_id = request.GET.get('shipment')
        transporter = Transporter.objects.get(id= trans_id)
        shipment = Shipment.objects.get(id = shipment_id)
        
        return JsonResponse({'company_name': transporter.company_name,
                             'ep': shipment.earliest_pickup_date,
                             'ld': shipment.latest_delivery_date,
                             'ed': shipment.earliest_delivery_date,
                             'lp': shipment.latest_pickup_date,
                             'quote': Quotes.objects.filter(shipment_id = shipment_id).filter(transporter_id = trans_id).values()[0]['quote']}, status = 200)

@csrf_exempt
def display_history_trans(request, id, status):
    if request.method == "GET":
        li = []
        if status == "Accepted":
            shipments = Shipment.objects.filter(transporter = Transporter.objects.get(id = id)).filter(is_accepted = True)
            li = list(shipments.values())
            print(li)
        else:
            shipments = Shipment.objects.filter(transporter = Transporter.objects.get(id = id)).filter(is_delivered = True)
            li = list(shipments.values())
    return JsonResponse({'data': li }, status=200)

@csrf_exempt
def confirm_shipment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transporter_id = data.get('trans_id')
        shipment_id = data.get('ship_id')
        
        shipment = Shipment.objects.get(id = shipment_id)
        shipment.transporter = Transporter.objects.get(id = int(transporter_id))
        shipment.is_accepted = True
        shipment.save()
        return JsonResponse({'data':'data'}, status=202)

@csrf_exempt
def display_quotes(request, id):
    if request.method == "GET":
        quotes = Quotes.objects.filter(shipment = Shipment.objects.get(id = id))
        data = list(quotes.values())
        i = 0
        for quote in quotes:
            data[i]["transporter_name"] = Transporter.objects.get(id = data[i]["transporter_id"]).company_name
            i += 1
        print(data)
        return JsonResponse({'data': data}, status=200)

@csrf_exempt
def deleteorder(request, id, user_id):
    if request.method == "DELETE":
        shipment = Shipment.objects.filter(id = id).filter(customer = Customer.objects.get(id = user_id))
        print(shipment.values())
        shipment.delete()
        return JsonResponse({'message': 'Shipment deleted successfully'}, status=204)
@csrf_exempt
def filterShipment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pickup = data.get('pickup')
        delivery = data.get('delivery')
        weight = data.get('weight')
        category = data.get('category')
        print(data)
        shipments = Shipment.objects.filter(Pickup = pickup).filter(Drop = delivery).filter(Weight = weight).filter(category = category)
        
        
        return JsonResponse({'data': list(shipments.values())}, status=200)



@method_decorator(csrf_exempt, name='dispatch')
class AddShipmentData(APIView):
    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('Shipment not created', status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):
        shipment_data = Shipment.objects.get(pk=id)
        serializer = ShipmentSerializer(shipment_data,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Shipment not updated', status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def login(request):
    
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
        
#         #user = authenticate(username=username, password=password)
#         print(username, password)
#         return JsonResponse({'message': 'Login successful'}, status=200)
#         """
#         else:
#             # Authentication failed
#             return JsonResponse({'error': 'Invalid username or password'}, status=400)
#         """
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)





# def find_shipments():
#     shipments = Shipment.objects.all()
  
    
        
#     print("Query results:", list(shipments))

   
# def cust_register(request):
#     if request.method == 'POST':
#         #this wont work
#         user = authenticate(phone=request.POST['phno'], password=request.POST['password'])   
#         if user is None:
#             Customer.objects.create(phno=request.POST['phno'], password_hash=request.POST['password'])
#         else:
#             return JsonResponse({'error': 'User already exists'}, status=400)
#         return JsonResponse({'message': 'User created successfully'}, status=201)        
    
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
@csrf_exempt
def shipper_temp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        t = Transporter()
        t.name = name
        t.email = email
        t.phone = phone
        t.save()

        #user = authenticate(username=request.POST['username'], password=request.POST['password'])   
        # if user is None:
        #     Transporter.objects.create(username=request.POST['username'], password_hash=request.POST['password'])
        # else:
        #     return JsonResponse({'error': 'User already exists'}, status=400)
        return JsonResponse({'message': 'User created successfully', "id": t.id}, status=201)        
    elif request.method == 'PUT':
        data = json.loads(request.body)
        print(data)
        id  = int(data.get("id"))
        owner = Transporter.objects.get(id = id)
        for (key, value) in data.items():
            setattr(owner, key, value)
        owner.save()
        return JsonResponse({'message': 'User updated successfully','owner':owner.company_name},status=206)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    # @csrf_exempt
# def addData(request): 
#     if request.method == 'POST':
#         # data = json.loads(request.body)
#         type=request.POST.get('Type')
#         length=request.POST.get('Length')
#         width=request.POST.get('Width')
#         weight=request.POST.get('Weight')
#         height=request.POST.get('Height')
#         quantity=request.POST.get('Quantity')
#         pickup=request.POST.get('Pickup')
#         drop=request.POST.get('Drop')
#         customer_id = request.POST.get('customer_id')
#         p_pincode = request.POST.get('p_pincode')
#         d_pincode = request.POST.get('d_pincode')
#         obj=Shipment()
#         obj.Type=type
#         obj.Length=length
#         obj.Width=width
#         obj.Height=height
#         obj.Quantity=quantity
#         obj.Pickup = pickup
#         obj.Drop = drop
#         obj.Weight = weight
#         obj.customer = Customer.objects.get(id = int(customer_id))
#         obj.p_pincode = p_pincode
#         obj.d_pincode = d_pincode
#         obj.save()
#         print(obj.customer.email)
#         return JsonResponse({"id":str(obj.pk), "type":obj.Type,"pickup":obj.Pickup,"drop":obj.Drop}, status=201)
#     elif request.method == 'PUT':
#         data = json.loads(request.body.decode('utf-8'))
#         id = data.get('id')
#         title = data.get('title')
#         latest_pickup_date = data.get('latest_pickup_date')
#         earliest_pickup_date = data.get('earliest_pickup_date')
#         earliest_delivery_date = data.get('earliest_delivery_date')
#         latest_delivery_date = data.get('latest_delivery_date')
#         image = request.FILES.get('photo')


#         try:
#             shipment = Shipment.objects.get(id=id)
#             shipment.title = title
#             shipment.latest_pickup_date = latest_pickup_date
#             shipment.earliest_pickup_date = earliest_pickup_date
#             shipment.earliest_delivery_date = earliest_delivery_date
#             shipment.latest_delivery_date = latest_delivery_date
#             if image:
#                 shipment.photo = image
#             shipment.save()
#             return JsonResponse({'message': 'Shipment updated successfully'}, status=206)
#         except Shipment.DoesNotExist:
#             return JsonResponse({'error': 'Shipment matching query does not exist'}, status=404)

#     # return JsonResponse({'error': 'Invalid request method'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
# # def updateData(request, id):
# #     mydata=Shipment.objects.get(id=id)

# #     return render(request, 'update.html', {'data':mydata})