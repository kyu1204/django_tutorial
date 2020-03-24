from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member


class SignUp(APIView):
    def post(self, request):
        try:
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

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': e.__str__()})


class IdCheck(APIView):
    def get(self, request):
        try:
            _id = request.query_params.get('id')
            idcheck = not User.objects.filter(username=_id).exists()
            if _id is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})
            else:
                return Response({"result": idcheck})

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': e.__str__()})


class SignIn(APIView):
    def post(self, request):
        try:
            if 'id' not in request.data or 'password' not in request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})

            _id = request.data['id']
            pw = request.data['password']

            UserModel = get_user_model()
            user = UserModel._default_manager.get_by_natural_key(_id)

            if user is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"result": None})

            if not user.check_password(raw_password=pw):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"result": None})

            if not user.is_active:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"result": "not_auth"})

            user = authenticate(username=_id, password=pw)
            if user is not None:
                login(request, user)
                return Response({'result': True})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'not found paramas'})

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': e.__str__()})


class SignOut(APIView):
    def get(self, request):
        try:
            logout(request)
            return Response({"result": True})

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': e.__str__()})
