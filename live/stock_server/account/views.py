from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member


class SignUp(APIView):
    def post(self, request):
        if 'id' not in request.data or 'password' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})

        if 'name' not in request.data or 'birthday' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})

        _id = request.data['id']
        pw = request.data['password']
        name = request.data['name']
        birthday = request.data['birthday']

        user = User.objects.create_user(username=_id, password=pw)
        user.is_active = False
        user.save()

        member = Member()
        member.create(user=user, name=name, birthday=birthday)
        member.save()

        return Response({'result': True})


class IdCheck(APIView):
    def get(self, request):
        _id = request.query_params.get('id')
        idcheck = not User.objects.filter(username=_id).exists()
        if _id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})
        else:
            return Response({"result": idcheck})


class SignIn(APIView):
    def post(self, request):
        if 'id' not in request.data or 'password' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})

        _id = request.data['id']
        pw = request.data['password']

        user = authenticate(username=_id, password=pw)
        if user is not None:
            login(request, user)
            return Response({'result': True})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})


class SignOut(APIView):
    def get(self, request):
        logout(request)
        return Response({"result": True})
