from membership.models import Membership, UserMembership, Subscription
from membership.models import Membership, UserMembership, Subscription


def get_all_active_premium_membership():
    active_premium_members = Subscription.objects.filter(active=True).filter(
        user_membership__membership__membership_type="PREMIUM"
    )
    return active_premium_members


def get_all_inactive_premium_membership():
    inactive_premium_members = Subscription.objects.filter(active=False).filter(
        user_membership__membership__membership_type="PREMIUM"
    )
    return inactive_premium_members


def get_all_active_trial_membership():
    active_trial_members = Subscription.objects.filter(active=True).filter(
        user_membership__membership__membership_type="TRIAL"
    )
    return active_trial_members


def get_all_inactive_trial_membership():
    inactive_trial_members = Subscription.objects.filter(active=False).filter(
        user_membership__membership__membership_type="TRIAL"
    )
    return inactive_trial_members


def get_all_active_membership():
    active_membership = Subscription.objects.filter(active=True)
    active_member_list = []
    for member in active_membership:
        active_member_list.append(member.user_membership.user.email)
    return active_member_list
