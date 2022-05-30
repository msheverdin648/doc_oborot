from django.urls import path
 
from .views import (
    SignUpView,
    PersonalListView,
    PersonalDeleteView,
    SearchPersonal,
)

urlpatterns = [
    path('signup_new_user/', SignUpView.as_view(), name='signup'),
    path('personal_list/', PersonalListView.as_view(), name='personal'),
    path('personal_delete/<int:user_id>/', PersonalDeleteView.as_view(), name='personal_delete'),
    path('search_personal/', SearchPersonal.as_view(), name='search_personal'),
]