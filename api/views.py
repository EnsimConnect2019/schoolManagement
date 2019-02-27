from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain

# Create your views here.
from django.http import JsonResponse

from rest_framework import generics, status, viewsets, permissions, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ClassName, Subject, ClassRoom, ChildParentsRelation, Holiday
from api.serializers import UserSerializer, ClassNameSerializers, SubjectSerializers, ClassRoomSerializers, HolidaySerializers


# This api will be call by admin user for "Add User", "List User" & "Group wise list user"
class UserCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        queryset = User.objects.all()
        groupname = self.request.query_params.get('role', None)
        if groupname is not None:
            try:
                group = Group.objects.get(name=groupname)
                queryset = group.user_set.all()
            except ObjectDoesNotExist:
                return Response(data={"msg": "Please provide valid role name"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# Admin can view all user profile and update users profile
# Owner can view their profile and update their profile
# Link: http://10.195.37.114:8000/api/users/3
class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if str(request.user.username) == str(instance) or request.user.is_superuser:
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"msg": "Unauthorized Access"})

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if str(request.user.username) == str(instance) or request.user.is_superuser:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"msg": "Unauthorized Access"})


class LoginView(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            group_name = user.groups.all()[0]
            return Response({'token': user.auth_token.key, 'userid': user.id, "role": group_name.name})
        else:
            return Response({'error': "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# This api will be used by all user to see list of classes
# Path: api/classes
class ClassNameView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassNameSerializers
    queryset = ClassName.objects.all()

class SubjectView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, permissions.DjangoModelPermissions)
    serializer_class = SubjectSerializers
    queryset = Subject.objects.all()

class ClassRoomView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser, permissions.DjangoModelPermissions)
    serializer_class = ClassRoomSerializers
    queryset = ClassRoom.objects.all()

class ChildParentsRelationView(APIView):

    def get(self, request):
        group = Group.objects.get(name="Parent")
        parents = group.user_set.values("id", "first_name", "last_name")
        parents = list(parents)


        group = Group.objects.get(name="Student")

        students = group.user_set.values("id","first_name","last_name")
        students = list(students)

        print({"parent" : parents, "student": students})

        return JsonResponse({"parent" : parents, "student": students},safe=False)



class HolidayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser, permissions.DjangoModelPermissions)
    serializer_class = HolidaySerializers
    queryset = Holiday.objects.all()


