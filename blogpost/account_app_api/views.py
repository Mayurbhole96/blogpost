from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from django.contrib.auth.models import User
import jwt, datetime

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# Create your views here.

# def check_token(view_func):
#     def wrapper(request, *args, **kwargs):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')
#         try:
#             payload = jwt.decode(token, 'secret', algorithm=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')
#         return view_func(request, *args, **kwargs)
#     return wrapper

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer.data:
            return Response({"status": "success", "data": {'items': serializer.data}}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"Record Not Available"}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
        password = request.data['password']
        email=""
        username=""
        try:
            email = request.data['email']
        except:
            username = request.data['username']
        
        if email:
            user = User.objects.filter(email=email).first()  
        elif username:  
            user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

# @method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    
    # @method_decorator(check_token)
    def get(self, request):
        user_obj =User.objects.filter(is_active__in = [True]).order_by('-id')
        serializer = UserSerializer(user_obj, many=True)
        if serializer.data:
            return Response({"status": "success", "data": {'items': serializer.data}}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"Record Not Available"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# def response_data(serilizer_obj,page,queryset):
#     page = int(page)
#     page_size = 10
#     # page_number = request.query_params.get('page', 2)
#     start_index = (page - 1) * page_size
#     end_index = start_index + page_size
#     my_models = queryset[start_index:end_index]
#     serializer = serilizer_obj(my_models, many=True)
#     return serializer.data