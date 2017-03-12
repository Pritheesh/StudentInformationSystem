from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from InfoSystem.models import Parent, Student, Result, Subject, CustomUser
from django.utils.translation import ugettext as _


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', )


class ResultSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(source='subject', read_only=True)
    class Meta:
        model = Result
        fields = ('subjects', 'internal_marks', 'external_marks', 'results', 'credits')

class StudentSerializer(serializers.ModelSerializer):
    stud_results = ResultSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = ('name', 'email', 'hall_ticket', 'stud_results')


class ParentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password', 'is_student']

    def create(self, validated_data):
        if validated_data['is_student'] is False:
            par = Parent.objects.get(mobile__exact=validated_data['mobile'])
            user = super(ParentRegisterSerializer, self).create(validated_data)
            par.user = user
            par.email = validated_data['email']
            par.is_registered=True
            par.save()
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            stud = Student.objects.get(mobile__exact=validated_data['mobile'])
            user = super(ParentRegisterSerializer, self).create(validated_data)
            stud.user = user
            stud.is_registered = True
            stud.save()
            user.set_password(validated_data['password'])
            user.save()
            return user

    def validate(self, data):
        if data['is_student'] is False:
            par = Parent.objects.get(mobile__exact=data['mobile'])
            if par.is_registered:
                raise serializers.ValidationError("You are already registered")
        else:
            stud = Student.objects.get(mobile__exact=data['mobile'])
            if stud.is_registered:
                raise serializers.ValidationError("You are already registered")
        return data


# class StudentUser(User):
#     hall_ticket = models.CharField(max_length=10)
#
# class StudentRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = StudentUser
#         fields = ['username', 'email', 'hall_ticket', 'password']
#
#     def create(self, validated_data):
#         stud = Student.objects.get(hall_ticket__iexact=validated_data['hall_ticket'])
#         if stud.is_registered == False:
#             user = super(StudentRegisterSerializer, self).create(validated_data)
#             stud.user = user
#             stud.is_registered=True
#             stud.save()
#             user.set_password(validated_data['password'])
#             user.save()
#             return user
#         return stud.user
#
#     def validate(self, data):
#         stud = Student.objects.get(hall_ticket__iexact=data['hall_ticket'])
#         if stud.is_registered:
#             raise serializers.ValidationError("You are already registered")
#         return data