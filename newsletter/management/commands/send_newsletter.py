#!/usr/bin/env python3
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from typing import Any, Dict, List

from blog.models import Article
from newsletter.models import SubscribedUsers

import config.settings as Settings


class Command(BaseCommand):
    help: str = ('Send newsletter to subscribers')

    def handle(self, *args: Any, **options: Any) -> None:
        '''Main method of custom command'''

        article_list = self._get_week_articles()
        subscriber_list = self._get_subscriber_list()
        self._send_mail(article_list, subscriber_list)

    def _get_week_articles(self) -> List[Dict]:
        '''Get all the articles published the last week.
        
        Returns: List[Dict] A list containing the articles 
            informations to send in the newsletter.
        '''
        week_start_date = timezone.now() - timezone.timedelta(6)
        week_articles = Article.objects.filter(publication_date__gte=week_start_date)
        article_list = []
        for article in week_articles:
            article_list.append(
                {
                    'id': article.id,
                    'title': article.title,
                    'author': f'{article.author.first_name} {article.author.last_name}',
                    'publication_date': article.publication_date,
                }
            )
        return article_list

    def _get_subscriber_list(self) -> List[Dict]:
        '''Get all the newsletter subscribers mails.

        Returns: List[str] Containing the subscribers emails.
        '''
        subscribers = SubscribedUsers.objects.all()
        subscriber_list = []
        for subscriber in subscribers:
            subscriber_list.append({"email": subscriber.email, "id": subscriber.id})
        return subscriber_list

    def _send_mail(
        self, article_list: List[Dict], subscribers_list: List[Dict],
    ) -> None:
        '''Send the newsletter to subscribers.
        
        Args:
            article_list (List[Dict]): The newsletter informations.
            subscribers_list (List[str]): The newsletter subscribers emails.

        '''
        subject: str = f"EasyWod - Les articles de la semaine!"
        email_template_name: str = "newsletter/newsletter_email.html"

        for subscriber_info in subscribers_list:
            c: dict = {
                "article_list": article_list,
                "protocol": "https",
                "domain": "easywod.angogg.com",
                "user_id": urlsafe_base64_encode(force_bytes(subscriber_info["id"])),
            }
            email: str = render_to_string(email_template_name, c)
            try:
                msg = EmailMessage(
                    subject,
                    email,
                    Settings.DEFAULT_FROM_EMAIL,
                    [subscriber_info["email"]],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()

            except BadHeaderError:
                print("Paramètres invalides.")
