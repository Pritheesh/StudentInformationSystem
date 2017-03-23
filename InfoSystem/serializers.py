from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from InfoSystem.models import Parent, Student, Result, Subject, CustomUser, ExamInfo, AchievementInASemester, \
    AchievementInASubject
from django.utils.translation import ugettext as _


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('is_student', )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', )


class ResultSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(source='subject', read_only=True)
    class Meta:
        model = Result
        fields = ('subjects', 'internal_marks', 'external_marks', 'results', 'credits')


class ExamInfoSerializer(serializers.ModelSerializer):
    result = ResultSerializer(many=True)
    class Meta:
        model = ExamInfo
        fields = ('year_of_pursue', 'semester', 'month_of_year', 'year_of_calendar', 'supple', 'year_of_pursue_roman', 'semester_roman', 'result')


class ResultSerializer2(serializers.ModelSerializer):
    subjects = SubjectSerializer(source='subject', read_only=True)
    class Meta:
        model = Result
        fields = ('subjects',)


class ExamInfoSerializer2(serializers.ModelSerializer):
    # result = ResultSerializer2(many=True)
    class Meta:
        model = ExamInfo
        fields = ('year_of_pursue', 'semester', 'month_of_year', 'year_of_calendar')


class AchievementInASemesterSerializer(serializers.ModelSerializer):
    examinfo = ExamInfoSerializer2()
    class Meta:
        model = AchievementInASemester
        fields = ('rank', 'examinfo')


class AchievementInASubjectSerializer(serializers.ModelSerializer):
    result = ResultSerializer2()
    class Meta:
        model = AchievementInASubject
        fields = ('rank', 'semester', 'year_of_pursue', 'result')


class StudentSerializer(serializers.ModelSerializer):
    examinfo = ExamInfoSerializer(many=True, read_only=True)
    achievementinasemester = AchievementInASemesterSerializer(many=True)
    ach_subject = AchievementInASubjectSerializer(many=True)
    class Meta:
        model = Student
        fields = ('name', 'email', 'hall_ticket', 'examinfo', 'achievementinasemester', 'ach_subject')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,  style={'input_type': 'password'})
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password', 'is_student']

    def create(self, validated_data):
        if validated_data['is_student'] is False:
            par = Parent.objects.get(mobile__exact=validated_data['mobile'])
            user = super(UserRegisterSerializer, self).create(validated_data)
            par.user = user
            par.email = validated_data['email']
            par.is_registered=True
            par.save()
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            stud = Student.objects.get(mobile__exact=validated_data['mobile'])
            user = super(UserRegisterSerializer, self).create(validated_data)
            stud.user = user
            stud.is_registered = True
            stud.save()
            user.set_password(validated_data['password'])
            user.save()
            return user

    def validate(self, data):
        if data['is_student'] is False:
            try:
                par = Parent.objects.get(mobile__exact=data['mobile'])
            except:
                raise serializers.ValidationError("Invalid mobile number.")
            if par.is_registered:
                raise serializers.ValidationError("You are already registered with the given mobile number.")
        else:
            try:
                stud = Student.objects.get(mobile__exact=data['mobile'])
            except:
                raise serializers.ValidationError("Invalid mobile number.")
            if stud.is_registered:
                raise serializers.ValidationError("You are already registered with the given mobile number.")
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