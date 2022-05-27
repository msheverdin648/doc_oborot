from django.urls import path
 
from .views import (
    SignUpView,
    PersonalListView,
    PersonalEditView,
    PersonalDeleteView,
    SearchPersonal,
    HomeView
)

urlpatterns = [
    path('signup_new_user/', SignUpView.as_view(), name='signup'),
    path('personal_list/', PersonalListView.as_view(), name='personal'),
    path('personal_edit/<int:user_id>/', PersonalEditView.as_view(), name='personal_edit'),
    path('personal_delete/<int:user_id>/', PersonalDeleteView.as_view(), name='personal_delete'),
    path('search_personal/', SearchPersonal.as_view(), name='search_personal'),
    path('', HomeView.as_view(), name='home')
]