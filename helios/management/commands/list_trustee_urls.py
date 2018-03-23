"""
verify cast votes that have not yet been verified

Ben Adida
ben@adida.net
2010-05-22
"""
import csv, datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from helios import utils as helios_utils
from helios.models import *

class Command(BaseCommand):
    args = ''
    help = 'List the voter login urls'

    def handle(self, *args, **options):
        if args:
            election = Election.objects.get(uuid=args[0])
            trustees = Trustee.objects.filter(election=election)
        else:
            trustees = Trustee.objects.all()

        for t in trustees:
            print t.election.uuid, t.get_login_url()
        # once broken out of the while loop, quit and wait for next invocation
        # this happens when there are no votes left to verify
