from django.urls import path, include
from . import views

app_name = 'membership'

urlpatterns = [
    path(r"<int:pk>", views.UserMembershipView.as_view(), name='select'),
    path(r"", views.UpdateMemberShipView.as_view(), name='change'),
    path(r"deactivate", views.DeactivateMemberShipView.as_view(), name='deactivate',),
]
