"""
verify cast votes that have not yet been verified

Ben Adida
ben@adida.net
2010-05-22
"""


from django.core.management.base import BaseCommand

from helios.models import Election, Voter


class Command(BaseCommand):
    args = ''
    help = 'List the voter login urls'

    def handle(self, *args, **options):
        if args:
            election = Election.objects.get(uuid=args[0])
            voters = Voter.objects.filter(poll__in=election.polls.all())
        else:
            voters = Voter.objects.all()

        for v in voters:
            print(v.poll.uuid, v.get_quick_login_url())
        # once broken out of the while loop, quit and wait for next invocation
        # this happens when there are no votes left to verify
