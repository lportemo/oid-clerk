from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings

from social_django.models import UserSocialAuth

import jwt
import datetime
import hmac
from hashlib import sha256

ALGO = 'HS256'

PUBLIC_KEY = settings.CLERK_PUBLIC_KEY
PRIVATE_KEY = settings.CLERK_PRIVATE_KEY

HMAC_KEY = str.encode(settings.HMAC_KEY)


def set_cookie(response, key, value):
    max_age = 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)


def get_digest(uid, host, port, room):
    return hmac.new(HMAC_KEY, str.encode(f'{uid}, {host}, {port}, {room}'), sha256).hexdigest()


@login_required
def craft(request):
    social_user = get_object_or_404(UserSocialAuth, user=request.user)
    uid = social_user.uid
    host = social_user.extra_data['ws_host']
    port = social_user.extra_data['ws_port']
    port_viewer = port
    room = social_user.extra_data['ws_room']
    #uid, host, port, room = 'toto', 'localhost', '4242', 'midlab'

    payload = { 'digest': get_digest(uid, host, port, room) }
    jwt_encoded = encoded_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm=ALGO).decode()


    response = HttpResponse('', status=200)
    for key, value in [('jwt', jwt_encoded), ('WS_UID', uid), ('WS_HOST', host),
                       ('WS_PORT', port), ('WS_ROOM', room), ('WS_PORT_VIEWER', port_viewer)]:
        set_cookie(response, key, value)
    return response


def check(request):
    for key in ['jwt', 'WS_UID', 'WS_HOST', 'WS_PORT', 'WS_ROOM']:
        if key not in request.COOKIES:
            return HttpResponse('', status=403)
    decoded = jwt.decode(request.COOKIES['jwt'], PUBLIC_KEY, algorithms=ALGO)
    if decoded['digest'] != get_digest(request.COOKIES.get('WS_UID'), request.COOKIES.get('WS_HOST'), request.COOKIES.get('WS_PORT'), request.COOKIES.get('WS_ROOM')):
        return HttpResponse('', status=403)
    return HttpResponse('', status=200)

