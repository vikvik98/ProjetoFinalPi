from django.contrib.auth.decorators import login_required
from django.urls import path

from perfil import views
from perfil.views import DisableProfileView
from usuarios.views import enable, activate_profile

urlpatterns = [
    path('<int:profile_id>', views.show_profile, name='show_profile'),
    path('logged/', views.show_logged_profile, name='show_logged_profile'),
    path('invite/<int:profile_id>', views.invite, name='invite'),
    path('cancel-invitation/<int:invitation_id>', views.cancel_invitation, name='cancel_invitation'),
    path('remove-friend/<int:profile_id>', views.undo_friendship, name='undo_friendship'),
    path('invitation/accept/<int:invitation_id>', views.accept, name='accept'),
    path('invitation/decline/<int:invitation_id>', views.decline, name='decline'),
    path('make-superuser/<int:profile_id>', views.make_superuser, name='make_superuser'),
    path('logged/give-up-superuser', views.give_up_superuser, name='give_up_superuser'),
    path('block-user/<int:profile_id>', views.block_user, name='block_user'),
    path('unblock-user/<int:profile_id>', views.unblock_user, name='unblock_user'),
    path('search-profile/', views.search_profile, name='search_profile'),
    path('blockers-profile/', views.show_blockers_profile, name='blockers_profile'),
    path('logged/disable', login_required(DisableProfileView.as_view()), name='disable_profile'),
    path('enable-profile/<int:id>', activate_profile, name='activate_profile'),
]
