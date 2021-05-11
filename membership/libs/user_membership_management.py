from membership.models import Membership, UserMembership
from user.models import User


def create_user_trial_membership(user_id):
    user = User.objects.get(id=user_id)

    free_membership = Membership.objects.get(membership_type='TRIAL')

    user_membership = UserMembership.objects.create(
        user=user,
        membership=free_membership,
        remaining_trial_courses=free_membership.trial_courses,
    )
    user_membership.save()

    return user_membership

