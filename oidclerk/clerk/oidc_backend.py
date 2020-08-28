from social_core.backends.open_id_connect import OpenIdConnectAuth
from django.conf import settings

class ProloginFinaleOpenIdConnect(OpenIdConnectAuth):
    name = "oidclerk"
    OIDC_ENDPOINT = settings.OIDC_ENDPOINT
    DEFAULT_SCOPE = ['openid', 'profile', 'email', 'workspace']
    ID_TOKEN_ISSUER = (OIDC_ENDPOINT,)
    USERNAME_KEY = 'ws_uid'

    def get_user_details(self, response):
        username_key = self.setting('USERNAME_KEY', default=self.USERNAME_KEY)
        return {
            'username': response.get(username_key),
            'ws_host': response.get('ws_host'),
            'ws_port': response.get('ws_port'),
            'ws_room': response.get('ws_room'),
        }
