import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse

from django.core.management.base import BaseCommand, CommandError

from ... import app_settings

class Command(BaseCommand):
    help = "Notify KeyError of a new deployment."
    args = '[options] "<deployment title>" "<deployment url>"'
    requires_model_validation = False

    def handle(self, *args, **options):
        if not app_settings.ENABLED:
            raise CommandError("KeyError is not enabled; exiting.")

        post_url = app_settings.URL % '/deployments'

        try:
            title, url = args
        except ValueError:
            raise CommandError("Invalid arguments: %s" % self.args)

        req = urllib.request.Request(post_url, urllib.parse.urlencode({
            'url': url,
            'title': title,
        }), {
            'X-API-Key': app_settings.SECRET_KEY,
        })

        try:
            urllib.request.urlopen(req, timeout=5)
        except urllib.error.HTTPError as exc:
            raise CommandError("Error when notifying KeyError: %s" % exc)
