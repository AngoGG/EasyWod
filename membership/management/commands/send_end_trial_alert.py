#!/usr/bin/env python3
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from typing import Any, Dict, List
from membership.libs import membership_queries

import config.settings as Settings


class Command(BaseCommand):
    help: str = ('Send newsletter to subscribers')

    def handle(self, *args: Any, **options: Any) -> None:
        '''Main method of custom command'''

        previous_day_ended_trials = membership_queries.get_previous_day_ended_trial()
        self._send_mail(previous_day_ended_trials)

    def _send_mail(self, user_list: List[Dict],) -> None:
        '''Send the newsletter to subscribers.
        
        Args:
            article_list (List[Dict]): The newsletter informations.
            subscribers_list (List[str]): The newsletter subscribers emails.

        '''
        subject: str = f"EasyWod - Fin de votre offre d'essai !"
        email_template_name: str = "membership/ending_trial_email.html"

        c: dict = {
            "protocol": "https",
            "domain": "easywod.angogg.com",
        }

        for user in user_list:
            email: str = render_to_string(email_template_name, c)
            try:
                msg = EmailMessage(subject, email, Settings.DEFAULT_FROM_EMAIL, [user],)
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()

            except BadHeaderError:
                print("Paramètres invalides.")
