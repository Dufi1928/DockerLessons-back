from django.urls import path
from .views import Register, Login, GetUsersNotif, CheckIfUserExist, UserDetail, checkLoginView, UserView

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('checkjwt', UserView.as_view()),
    path('checkLoginView', checkLoginView.as_view()),
    path('checkIfUserExist', CheckIfUserExist.as_view()),
    path('user-detail/<int:user_id>', UserDetail.as_view()),
    path('pseudos', GetUsersNotif.as_view()),
]
