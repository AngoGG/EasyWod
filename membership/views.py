from django.contrib import messages  # import messages
from django.shortcuts import redirect
from django.views.generic import ListView

from membership.models import Membership, UserMembership, Subscription


class MembershipView(ListView):
    model = Membership
    template_name = 'membership/list.html'

    def get_user_membership(self):
        user_membership_qs = UserMembership.objects.filter(user=self.request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = self.get_user_membership()
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request):

        selected_membership = Membership.objects.get(
            membership_type=self.request.POST['membership_type']
        )

        user_membership = UserMembership.objects.get(user=self.request.user)

        user_membership.membership = selected_membership

        user_membership.save()
        messages.success(
            request, "Le plan d'abonnement de l'utilisateur a bien été mis à jour",
        )
        return redirect("/")
