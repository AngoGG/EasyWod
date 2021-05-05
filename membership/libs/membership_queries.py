from django.utils import timezone
from membership.models import Membership, UserMembership
from membership.libs import membership_queries


def get_all_active_premium_membership():
    print(f'HELLO')
    active_premium_members = UserMembership.objects.filter(active=True).filter(
        membership__membership_type="PREMIUM"
    )
    print(f'active_premium_members : {active_premium_members}')
    return active_premium_members


def get_all_inactive_premium_membership():
    inactive_premium_members = UserMembership.objects.filter(active=False).filter(
        membership__membership_type="PREMIUM"
    )
    return inactive_premium_members


def get_all_active_trial_membership():
    active_trial_members = UserMembership.objects.filter(active=True).filter(
        membership__membership_type="TRIAL"
    )
    return active_trial_members


def get_all_inactive_trial_membership():
    inactive_trial_members = UserMembership.objects.filter(active=False).filter(
        membership__membership_type="TRIAL"
    )
    return inactive_trial_members


def get_all_active_membership():
    active_membership = UserMembership.objects.filter(active=True)
    active_member_list = []
    for membership in active_membership:
        active_member_list.append(membership.user.email)
    return active_member_list


def get_trial_to_deactivate():
    user_memberships = UserMembership.objects.filter(
        membership__membership_type="TRIAL", active=True, remaining_trial_courses=0,
    )
    user_email_list = []
    for user_membership in user_memberships:
        user_email_list.append(user_membership)
    return user_email_list


def get_previous_day_ended_trial():
    previous_day = timezone.now() - timezone.timedelta(1)
    user_memberships = UserMembership.objects.filter(
        membership__membership_type="TRIAL",
        active=False,
        unsubscription_date__year=previous_day.year,
        unsubscription_date__month=previous_day.month,
        unsubscription_date__day=previous_day.day,
    )

    user_email_list = []
    for previous_day_ended_trials in user_memberships:
        user_email_list.append(previous_day_ended_trials.user.email)
    return user_email_list
