from django.contrib import messages  # import messages
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, UpdateView

from membership.models import Membership, UserMembership
from user.models import User


class UserMembershipView(DetailView):
    model = User
    template_name = 'membership/list.html'
    context_object_name = "member"

    def get_user_membership(self, member):
        user_membership_qs = UserMembership.objects.filter(user=member)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = self.get_user_membership(context['member'])
        context['current_membership'] = str(current_membership.membership)
        context['membership_list'] = Membership.objects.all()
        print(f' LE CONTEXT : {context}')
        return context


class UpdateMemberShipView(UpdateView):
    def post(self, request, *args, **kwargs):

        selected_membership = Membership.objects.get(
            membership_type=self.request.POST['membership_type']
        )

        user_membership = UserMembership.objects.get(user=self.request.POST['member'])

        user_membership.membership = selected_membership

        user_membership.save()
        messages.success(
            request, "Le plan d'abonnement de l'utilisateur a bien été mis à jour",
        )
        return redirect("/")


class DeactivateMemberShipView(UpdateView):
    def post(self, request, *args, **kwargs):

        print(f'HELLO MDR')
        user_membership = UserMembership.objects.get(user=self.request.POST['member'])

        user_membership.active = False

        user_membership.save()
        messages.success(
            request, "L'abonnement de l'utilisateur a bien été désactivé",
        )
        return redirect("/")
