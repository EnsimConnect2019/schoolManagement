from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.db import IntegrityError
from django.http import JsonResponse

from rest_framework import generics, status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ClassName, Subject, ClassRoom, ChildParentsRelation, Holiday, StudentClass, Attendance
from api.serializers import UserSerializer, ClassNameSerializers, SubjectSerializers, ClassRoomSerializers,\
                            HolidaySerializers, StudentClassSerializers, AttendanceSerializers, AttSerializers


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

#userlist view
class UserListView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        user = User.objects.values("id", "username", "first_name", "last_name", "email")
        students = user.filter(groups__name="Student")
        teachers = user.filter(groups__name="Teacher")
        parents = user.filter(groups__name="Parent")
        context = {"Students": list(students), "Teachers": list(teachers), "Parents": list(parents)}
        return JsonResponse(context, status=status.HTTP_200_OK)


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


class HolidayView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser, permissions.DjangoModelPermissions)
    serializer_class = HolidaySerializers
    queryset = Holiday.objects.all()


class ChildParentsRelationView(APIView):
    permission_classes = {IsAuthenticated, IsAdminUser}

    def get(self, request):

        parents = list(User.objects.values("id", "first_name", "last_name").filter(groups__name="Parent"))
        students = User.objects.values("id", "first_name", "last_name").filter(groups__name="Student")
        students = list(students.exclude(id__in = ChildParentsRelation.objects.values("student")))

        return JsonResponse({"parents": parents, "students": students}, safe=False)

    def post(self, request):
        try:
            student = User.objects.filter(groups__name="Student").get(id = request.data.get("student"))
            parent = User.objects.filter(groups__name="Parent").get(id = request.data.get("parent"))
            record = ChildParentsRelation.objects.filter(student = student, parent= parent)
            if record:
                return JsonResponse({"detail": "Data already available"}, status=status.HTTP_302_FOUND)
            else:
                a = ChildParentsRelation(student= student, parent= parent)
                a.save()
                return JsonResponse({"detail": "Data saved successfully"},status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({"detail": "Please provide valid id"},status = status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({"detail": "Please provide valid student and parent id"}, status=status.HTTP_400_BAD_REQUEST)


class StudentClassView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = StudentClassSerializers
    queryset = StudentClass.objects.select_related("student").all()
    print(queryset.query)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.values("id","student_id","student__username","student__first_name","student__last_name",
                                        "student__email","session   _year","roll_no","class_name__class_text")
        print(queryset)
        return JsonResponse(list(queryset),status=status.HTTP_200_OK,safe=False)

class AttendanceView(APIView):

    def get(self, request, format=None):
        attlist = Attendance.objects.all()
        serializer = AttendanceSerializers(attlist, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        present = request.data.get("present")
        schedule = request.data['schedule']['id']
        student = request.data['student']['id']
        data = {'student': student, 'schedule': schedule, 'present': present}
        serializer = AttSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)