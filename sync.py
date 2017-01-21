import django
import sys, traceback
import os
from django.core import mail
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()
from mails.models import Offer

Offer_dbs = Offer.objects.raw("SELECT * FROM offers_copy")

for Offer_db in Offer_dbs:
    new = Offer(
        lead = Offer_db.lead,
        drop = Offer_db.drop,
        amount = Offer_db.amount,
        offer_id = Offer_db.offer_id,
        base_id = Offer_db.base_id,
        hash_base_id = Offer_db.hash_base_id,
        email = Offer_db.email,
        remail = Offer_db.remail,
        contact = Offer_db.contact,
        name = Offer_db.name,
        code = Offer_db.code,
        sale = Offer_db.sale,
        date_started = Offer_db.date_started,
        date = Offer_db.date,
        updated = Offer_db.updated,
        status = Offer_db.status,
        stage = Offer_db.stage,
        phase = Offer_db.phase,
        last_email_date = Offer_db.last_email_date,
    )

    new.save()
