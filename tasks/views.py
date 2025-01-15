from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error":"username and password is required!"},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error":"username already exists!"},status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username,password=password)
        return Response({"message":"user registered successfully!"},status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer  = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username =  serializer.validated_data['username']
            password = serializer.validated_data['password']
            print("username:",username)

            user = authenticate(request,username=username,password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'username': user.username,
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#filter class
class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES, label="Status")
    due_date = filters.DateFilter(field_name='due_date', lookup_expr='gte', label="Due Date (greater than or equal)")

    class Meta:
        model = Task
        fields = ['status', 'due_date']  


class TaskView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,task_id=None):   
        if task_id:
            try:
                task = Task.objects.filter(id=task_id,user=request.user)
                serializer = TaskSerializer(task,many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Task.DoesNotExist:
                return Response({"error": "Task not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            tasks = Task.objects.filter(user=request.user)
            
            task_filter = TaskFilter(request.query_params, queryset=tasks)
            tasks = task_filter.qs

            ordering = request.query_params.get('ordering', 'due_date') 
            allowed_ordering_fields = ['due_date', '-due_date', 'status', '-status', 'title', '-title']
            if ordering not in allowed_ordering_fields:
                return Response({"error": f"Invalid ordering field: {ordering}"}, status=status.HTTP_400_BAD_REQUEST)

            tasks = tasks.order_by(ordering)

            serializer = TaskSerializer(tasks,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request,task_id):
        try:
            task = Task.objects.get(id=task_id,user=request.user)
        except Task.DoesNotExist:
                return Response({"error": "Task not found!"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = TaskSerializer(task,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,task_id):
        try:
            task = Task.objects.get(id=task_id,user=request.user)
        except Task.DoesNotExist:
                return Response({"error": "Task not found!"}, status=status.HTTP_404_NOT_FOUND)
    
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
