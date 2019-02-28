"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import UserCreate, UserView, LoginView, ClassNameView, ChildParentsRelationView, UserListView

routerSubject = routers.DefaultRouter()
routerSubject.register('', views.SubjectView)

routerClassRoom = routers.DefaultRouter()
routerClassRoom.register('', views.ClassRoomView)

routerHoliday = routers.DefaultRouter()
routerHoliday.register('', views.HolidayView)

routerStudentClass = routers.DefaultRouter()
routerStudentClass.register('', views.StudentClassView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users', UserCreate.as_view()),
    path('api/users/<int:pk>', UserView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/classes/', ClassNameView.as_view()),
    path('api/subjects/', include(routerSubject.urls)),
    path('api/classrooms/', include(routerClassRoom.urls)),
    path('api/childparentsrelation/', ChildParentsRelationView.as_view()),
    path('api/holidays/', include(routerHoliday.urls)),
    path('api/studentclass/', include(routerStudentClass.urls))
]
