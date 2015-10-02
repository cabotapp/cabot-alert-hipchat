from django.db import models
from cabot.cabotapp.alert import AlertPlugin, AlertPluginUserData

from os import environ as env

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context, Template

import requests

hipchat_template = "Service {{ service.name }} {% if service.overall_status == service.PASSING_STATUS %}is back to normal{% else %}reporting {{ service.overall_status }} status{% endif %}: {{ scheme }}://{{ host }}{% url 'service' pk=service.id %}. {% if service.overall_status != service.PASSING_STATUS %}Checks failing: {% for check in service.all_failing_checks %}{% if check.check_category == 'Jenkins check' %}{% if check.last_result.error %} {{ check.name }} ({{ check.last_result.error|safe }}) {{jenkins_api}}job/{{ check.name }}/{{ check.last_result.job_number }}/console{% else %} {{ check.name }} {{jenkins_api}}/job/{{ check.name }}/{{check.last_result.job_number}}/console {% endif %}{% else %} {{ check.name }} {% if check.last_result.error %} ({{ check.last_result.error|safe }}){% endif %}{% endif %}{% endfor %}{% endif %}{% if alert %}{% for alias in users %} @{{ alias }}{% endfor %}{% endif %}"
hipchat_update_template = '@{{ service.unexpired_acknowledgement.user.hipchat_alias }} working on service {{ service.name }} (status {{ service.overall_status }}) - acknowledged @ {{ service.unexpired_acknowledgement.time|date:"H:i" }}'

# This provides the hipchat alias for each user. Each object corresponds to a User
class HipchatAlert(AlertPlugin):
    name = "Hipchat"
    author = "Jonathan Balls"

    def send_alert(self, service, users, duty_officers):
        alert = True
        hipchat_aliases = []
        users = list(users) + list(duty_officers)

        hipchat_aliases = [u.hipchat_alias for u in HipchatAlertUserData.objects.filter(user__user__in=users)]

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

        c = Context({
            'service': service,
            'users': hipchat_aliases,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            'alert': alert,
            'jenkins_api': settings.JENKINS_API,
        })
        message = Template(hipchat_template).render(c)
        self._send_hipchat_alert(
            message,
            color=color,
            sender='Cabot/%s' % service.name
        )

    def send_alert_update(self, service, users, duty_officers):
        users = list(users) + list(duty_officers)

        hipchat_aliases = [u.hipchat_alias for u in HipchatAlertUserData.objects.filter(user__user__in=users)]

        color = 'yellow'
        c = Context({
            'service': service,
            'users': hipchat_aliases,
            'host': settings.WWW_HTTP_HOST,
            'scheme': settings.WWW_SCHEME,
            'alert': False,
        })
        message = Template(hipchat_update_template).render(c)
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

class HipchatAlertUserData(AlertPluginUserData):
    name = "Hipchat Plugin"
    hipchat_alias = models.CharField(max_length=50, blank=True)

