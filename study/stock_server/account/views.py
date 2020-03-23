from django.contrib.auth.models import User
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
        user = User(username=_id, password=pw)
        user.is_active = False

        member = Member()
        member.create(user=user, name=name, birthday=birthday)
        member.save()

        return Response({'message': True})
