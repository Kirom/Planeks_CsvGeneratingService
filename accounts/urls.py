from django.urls import path

from accounts.views import logout_view, registration_view, UserPasswordResetView, \
    UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView, login_view, activate_account

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration_view, name='registration'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/<uidb64>/<token>/reset/done/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
]
