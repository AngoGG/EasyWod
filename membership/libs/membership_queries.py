from typing import List

from django.db.models.query import QuerySet
from django.utils import timezone

from membership.models import UserMembership


def get_all_active_premium_membership() -> QuerySet:
    return UserMembership.objects.filter(active=True).filter(
        membership__membership_type="PREMIUM"
    )


def get_all_inactive_premium_membership() -> QuerySet:
    return UserMembership.objects.filter(active=False).filter(
        membership__membership_type="PREMIUM"
    )


def get_all_active_trial_membership() -> QuerySet:
    return UserMembership.objects.filter(active=True).filter(
        membership__membership_type="TRIAL"
    )


def get_all_inactive_trial_membership() -> QuerySet:
    return UserMembership.objects.filter(active=False).filter(
        membership__membership_type="TRIAL"
    )


def get_all_active_membership() -> List[str]:
    '''Get all the active membership and returns their user email.
    '''

    active_membership = UserMembership.objects.filter(active=True)
    active_member_list = []
    for membership in active_membership:
        active_member_list.append(membership.user.email)
    return active_member_list


def get_trial_to_deactivate() -> QuerySet:
    '''Returns all the active trial membership 
    with no remaining course and returns.
    '''
    return UserMembership.objects.filter(
        membership__membership_type="TRIAL", active=True, remaining_trial_courses=0,
    )


def get_previous_day_ended_trial() -> List[str]:
    '''Get all trial than have been deactivated the previous day 
    and returns their user mail
    '''
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
