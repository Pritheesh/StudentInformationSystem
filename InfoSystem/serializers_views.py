from django.contrib.auth import get_user_model
from djoser.views import RegistrationView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from InfoSystem.models import Parent, Student
from InfoSystem.serializers import StudentSerializer, UserRegisterSerializer, CustomUserSerializer


class StudentList(APIView):

    def get(self, request, format=None):
        if request.user.is_student is False:
            parent = Parent.objects.get(user=request.user)
            students = parent.student_set.all()
            serializer = StudentSerializer(students, many=True)
        else:
            stud = Student.objects.get(user=request.user)
            serializer = StudentSerializer(stud)
        serializer2 = CustomUserSerializer(request.user)
        return Response({'user': serializer2.data, 'students': serializer.data})


class UserRegisterView(RegistrationView):
    model = get_user_model()
    permission_classes = (AllowAny, )
    serializer_class = UserRegisterSerializer
    def get_queryset(self):
        if self.queryset is None:
            raise Exception('User is already registered')

    def send_activation_email(self, user):
        RegistrationView.send_activation_email(self, user)
#
# class StudentRegisterView(CreateAPIView):
#     permission_classes = (AllowAny, )
#     serializer_class = StudentRegisterSerializer