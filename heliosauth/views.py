"""
Views for authentication

Ben Adida
2009-07-05
"""

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.conf import settings

from .view_utils import render_template
from heliosauth.security import get_user

from auth_systems import AUTH_SYSTEMS

import heliosauth
import urllib

from models import User
from security import FIELDS_TO_SAVE
from heliosauth.forms import ChangePasswordForm

def index(request):
    """
    the page from which one chooses how to log in.
    """

    user = get_user(request)

    # single auth system?
    if len(heliosauth.ENABLED_AUTH_SYSTEMS) == 1 and not user:
        return HttpResponseRedirect(reverse(start, args=[heliosauth.ENABLED_AUTH_SYSTEMS[0]])+ '?return_url=' + request.GET.get('return_url', ''))

    #if heliosauth.DEFAULT_AUTH_SYSTEM and not user:
    #  return HttpResponseRedirect(reverse(start, args=[heliosauth.DEFAULT_AUTH_SYSTEM])+ '?return_url=' + request.GET.get('return_url', ''))

    default_auth_system_obj = None
    if heliosauth.DEFAULT_AUTH_SYSTEM:
        default_auth_system_obj = AUTH_SYSTEMS[heliosauth.DEFAULT_AUTH_SYSTEM]

    #form = password.LoginForm()

    return render_template(request,'index', {'return_url' : request.GET.get('return_url', reverse('home')),
                                             'enabled_auth_systems' : heliosauth.ENABLED_AUTH_SYSTEMS,
                                             'default_auth_system': heliosauth.DEFAULT_AUTH_SYSTEM,
                                             'default_auth_system_obj': default_auth_system_obj})


def do_local_logout(request):
    """
    if there is a logged-in user, it is saved in the new session's "user_for_remote_logout"
    variable.
    """

    user = None

    if request.session.has_key('user'):
        user = request.session['user']

    # 2010-08-14 be much more aggressive here
    # we save a few fields across session renewals,
    # but we definitely kill the session and renew
    # the cookie
    field_names_to_save = request.session.get(FIELDS_TO_SAVE, [])

    # let's clean up the self-referential issue:
    field_names_to_save = set(field_names_to_save)
    field_names_to_save = field_names_to_save - set([FIELDS_TO_SAVE])
    field_names_to_save = list(field_names_to_save)

    fields_to_save = dict([(name, request.session.get(name, None)) for name in field_names_to_save])

    # let's not forget to save the list of fields to save
    fields_to_save[FIELDS_TO_SAVE] = field_names_to_save

    request.session.flush()

    for name in field_names_to_save:
        request.session[name] = fields_to_save[name]

    # copy the list of fields to save
    request.session[FIELDS_TO_SAVE] = fields_to_save[FIELDS_TO_SAVE]

    request.session['user_for_remote_logout'] = user

def do_remote_logout(request, user, return_url=None):
    # FIXME: do something with return_url
    if return_url is None:
        return_url = reverse('home')
    auth_system = AUTH_SYSTEMS[user['type']]

    # does the auth system have a special logout procedure?
    user_for_remote_logout = request.session.get('user_for_remote_logout', None)
    del request.session['user_for_remote_logout']
    if hasattr(auth_system, 'do_logout'):
        response = auth_system.do_logout(user_for_remote_logout)
        return response

def _do_auth(request):
    # the session has the system name
    system_name = request.session['auth_system_name']

    # get the system
    system = AUTH_SYSTEMS[system_name]

    # where to send the user to?
    redirect_url = "%s%s" % (settings.SECURE_URL_HOST,reverse(after))
    auth_url = system.get_auth_url(request, redirect_url=redirect_url)

    if auth_url:
        return HttpResponseRedirect(auth_url)
    else:
        return HttpResponse("an error occurred trying to contact " + system_name +", try again later")

def start(request, system_name):
    if not (system_name in heliosauth.ENABLED_AUTH_SYSTEMS):
        return HttpResponseRedirect(reverse(index))

    # why is this here? Let's try without it
    # request.session.save()

    # store in the session the name of the system used for auth
    request.session['auth_system_name'] = system_name

    # where to return to when done
    request.session['auth_return_url'] = request.GET.get('return_url', '/')

    return _do_auth(request)

def perms_why(request):
    if request.method == "GET":
        return render_template(request, "perms_why")

    return _do_auth(request)

def after(request):
    # which auth system were we using?
    if not request.session.has_key('auth_system_name'):
        do_local_logout(request)
        return HttpResponseRedirect(reverse('home'))

    system = AUTH_SYSTEMS[request.session['auth_system_name']]

    # get the user info
    user = system.get_user_info_after_auth(request)

    if user:
        # get the user and store any new data about him
        user_obj = User.update_or_create(user['type'], user['user_id'], user['name'], user['info'], user['token'])

        request.session['user'] = user_obj.pk
    else:
        return HttpResponseRedirect("%s?%s" % (reverse(perms_why), urllib.urlencode({'system_name' : request.session['auth_system_name']})))

    # does the auth system want to present an additional view?
    # this is, for example, to prompt the user to follow @heliosvoting
    # so they can hear about election results
    if hasattr(system, 'user_needs_intervention'):
        intervention_response = system.user_needs_intervention(user['user_id'], user['info'], user['token'])
        if intervention_response:
            return intervention_response

    # go to the after intervention page. This is for modularity
    return HttpResponseRedirect(reverse(after_intervention))

def after_intervention(request):
    return_url = reverse('home')
    if request.session.has_key('auth_return_url'):
        return_url = request.session['auth_return_url']
        del request.session['auth_return_url']
    return HttpResponseRedirect("%s%s" % (settings.URL_HOST, return_url))


def change_password(request):
    user = request.zeususer
    if not user or user.user_type != 'password':
        return HttpResponseRedirect(reverse('home'))

    password_changed = request.GET.get('password_changed', None)
    if not user.user_type == "password":
        return HttpResponseForbidden()

    form = ChangePasswordForm(user)
    if request.method == "POST":
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('change_password') + \
                                        '?password_changed=1')

    return render_template(request, 'change_password', {'form': form,
                                                        'password_changed': password_changed})
