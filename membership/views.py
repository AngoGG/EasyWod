from django.contrib import messages  # import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, View

from membership.models import Membership, UserMembership
from user.models import User


class UserMembershipView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

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
        return context


class UpdateMemberShipView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    def post(self, request, *args, **kwargs):

        selected_membership = Membership.objects.get(
            membership_type=self.request.POST['membership_type']
        )

        user_membership = UserMembership.objects.get(user=self.request.POST['member'])

        user_membership.membership = selected_membership

        if self.request.POST['membership_type'] == "PREMIUM":
            user_membership.subscribtion_date = timezone.now()

        user_membership.save()
        messages.success(
            request, "Le plan d'abonnement de l'utilisateur a bien été mis à jour",
        )
        return redirect("/")


class DeactivateMemberShipView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    def post(self, request, *args, **kwargs):

        user_membership = UserMembership.objects.get(user=self.request.POST['member'])

        user_membership.active = False
        user_membership.unsubscription_date = timezone.now()

        user_membership.save()

        messages.success(
            request, "L'abonnement de l'utilisateur a bien été désactivé",
        )
        return redirect("/")


class ReactivateMemberShipView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.type == "EMPLOYEE"
        )

    def post(self, request, *args, **kwargs):

        user_membership = UserMembership.objects.get(user=self.request.POST['member'])
        user_membership.active = True
        user_membership.unsubscription_date = None

        if user_membership.membership.membership_type == "PREMIUM":
            messages.success(
                request, f"L'abonnement de l'utilisateur a bien été réactivé",
            )
        else:
            user_membership.remaining_trial_courses = 3
            messages.success(
                request,
                f"L'abonnement de l'utilisateur avec {user_membership.remaining_trial_courses} cours supplémentaires.",
            )
        user_membership.save()

        return redirect("/")

