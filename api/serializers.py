from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import ClassRoom, Subject, ClassName, Holiday, StudentClass, Schedule, ScheduleTemplate,  Attendance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User(username=validated_data['username'], email=validated_data['email'],
                    first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])

        request = self.context.get("request")
        try:
            group = Group.objects.get(name=request.data.get("role"))
        except:
            raise serializers.ValidationError({"msg": "Please provide valid role"})
        user.save()
        user.groups.add(group)
        Token.objects.create(user=user)

        return user

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            if str(attr) == "password":
                instance.set_password(validated_data['password'])
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


class ClassRoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"
        queryset = ClassRoom.objects.all()


class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class ClassNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = "__all__"


class HolidaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"


class StudentClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = "__all__"


class ScheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class AttendanceSerializers(serializers.ModelSerializer):
    schedule = ScheduleSerializers(many=False, read_only=True)
    student = UserSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'present', 'schedule', 'student')


class AttSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
