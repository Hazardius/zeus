
from django.core.management.base import BaseCommand

from helios.models import Poll, Voter

class Command(BaseCommand):
    args = ''
    help = 'List the voter login urls'

    def handle(self, *args, **options):
        if args:
            poll = Poll.objects.get(uuid=args[0])
            voters = Voter.objects.filter(poll=poll)
        else:
            voters = Voter.objects.all()

        for v in voters:
            print v.get_quick_login_url()
        # once broken out of the while loop, quit and wait for next invocation
        # this happens when there are no votes left to verify
