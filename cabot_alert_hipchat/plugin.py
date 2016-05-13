from django.conf import settings
from django.core.urlresolvers import reverse
from cabot.plugins.models import AlertPlugin
from django import forms
from os import environ as env
import requests


class HipchatUserSettingsForm(forms.Form):
    hipchat_alias = forms.CharField(max_length=64)

class HipchatAlertPlugin(AlertPlugin):
    name = "Hipchat"
    slug = "cabot_alert_hipchat"
    author = "Jonathan Balls"
    version = "0.0.1"
    font_icon = "fa fa-comment"

    plugin_variables = [
        'HIPCHAT_ALERT_ROOM',
        'HIPCHAT_API_KEY'
    ]

    user_config_form = HipchatUserSettingsForm

    def send_alert(self, service, users, duty_officers):

        # Check whether to alert users (by appending their names to the end of
        # the message).
        alert = True
        if service.overall_status == service.WARNING_STATUS:
            alert = False  # Don't alert at all for WARNING
        if service.overall_status == service.ERROR_STATUS:
            if service.old_overall_status in (service.ERROR_STATUS, service.ERROR_STATUS):
                alert = False  # Don't alert repeatedly for ERROR
        if service.overall_status == service.PASSING_STATUS:
            color = 'green'
            if service.old_overall_status == service.WARNING_STATUS:
                alert = False  # Don't alert for recovery from WARNING status
        else:
            color = 'red'

        message = service.get_status_message()

        if alert:
            #users = list(users) + list(duty_officers)
            hipchat_aliases = [u.cabot_alert_hipchat_settings.hipchat_alias for u in users]
            for alias in hipchat_aliases:
                message = '{} @{}'.format(message, alias)

        self._send_hipchat_alert(
            message,
            color=color,
            sender='Cabot/%s' % service.name
        )

    def _send_hipchat_alert(self, message, color='green', sender='Cabot'):

        room = env.get('HIPCHAT_ALERT_ROOM')
        api_key = env.get('HIPCHAT_API_KEY')
        url = env.get('HIPCHAT_URL')

        resp = requests.post(url + '?auth_token=' + api_key, data={
            'room_id': room,
            'from': sender[:15],
            'message': message,
            'notify': 1,
            'color': color,
            'message_format': 'text',
	})

