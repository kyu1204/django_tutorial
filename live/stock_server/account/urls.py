from django.urls import path
from .views import SignUp, SignIn, SignOut, IdCheck

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('signin/', SignIn.as_view()),
    path('signout/', SignOut.as_view()),
    path('idcheck/', IdCheck.as_view()),
]
