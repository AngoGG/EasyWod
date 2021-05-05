#!/usr/bin/env python3
from django.core.management.base import BaseCommand
from membership.libs import membership_queries
from typing import Any, Dict, List
from django.utils import timezone


class Command(BaseCommand):
    help: str = ('Send newsletter to subscribers')

    def handle(self, *args: Any, **options: Any) -> None:
        '''Main method of custom command'''

        print(f'LANCEMENT COMMANDE')
        trials_to_deactivate = membership_queries.get_trial_to_deactivate()
        for trial_membership in trials_to_deactivate:
            trial_membership.active = False
            trial_membership.unsubscription_date = timezone.now()
            trial_membership.save()

