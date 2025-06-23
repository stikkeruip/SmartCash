from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.test_api, name='test_api'),
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/auth/profile/', views.ProfileView.as_view(), name='profile'),
    path('api/auth/personal-info/', views.PersonalInformationView.as_view(), name='personal_info'),
    path('api/auth/delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('api/bank/', views.BankOptionsView.as_view(), name='bank_options'),
    path('api/bank/piraeus/', views.PiraeusLinkingView.as_view(), name='piraeus_linking'),
]