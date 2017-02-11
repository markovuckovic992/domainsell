from datetime import datetime, timedelta
from mails.post_re_mails import *
from mails.models import controlPanel
from random import randint

def sequnce_0(stage, last_email_date):
    today = datetime.now()
    case = randint(1, 10)
    if stage == 1:
        margin = (today - timedelta(days=2)).date()
        if margin > last_email_date:
            return "pr_msg" + str(case)
        else:
            return None
    else:
        return None

def sequnce_1(stage, last_email_date):
    today = datetime.now()
    if stage < 6:
        distance = int(controlPanel.objects.get(tip=1, order=stage).distance)

    if stage == 1:
        return "po_msg1"

    elif stage == 2:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "po_msg2"
        else:
            return None

    elif stage == 3:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "po_msg3"
        else:
            return None

    elif stage == 4:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "po_msg4"
        else:
            return None

    elif stage == 5:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "po_msg5"
        else:
            return None

    else:
        return None

def sequnce_2(stage, last_email_date):
    today = datetime.now()
    if stage < 13:
        distance = int(controlPanel.objects.get(tip=2, order=stage).distance)
    if stage == 1:
        return "form_a_msg1"

    elif stage == 2:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg2"
        else:
            return None

    elif stage == 3:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg3"
        else:
            return None

    elif stage == 4:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg4"
        else:
            return None

    elif stage == 5:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg5"
        else:
            return None

    elif stage == 6:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg6"
        else:
            return None

    elif stage == 7:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg7"
        else:
            return None

    elif stage == 8:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg8"
        else:
            return None

    elif stage == 9:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg9"
        else:
            return None

    elif stage == 10:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg10"
        else:
            return None

    elif stage == 11:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg11"
        else:
            return None

    elif stage == 12:
        margin = (today - timedelta(days=distance)).date()
        if margin > last_email_date:
            return "form_a_msg12"
        else:
            return None

    else:
        return None
