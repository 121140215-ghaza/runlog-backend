from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from runlog_backend.auth_policy import JWTAuthenticationPolicy, get_user
from pyramid.tweens import MAIN



def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('runlog_backend.routes')
        config.include('runlog_backend.models')
        
        import logging
        logging.basicConfig()
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)
        log.debug("Registering CORS tween")

        # Jangan import, cukup daftarkan pakai path string
        config.add_tween('runlog_backend.cors.cors_tween_factory', over=MAIN) 

        # Setup JWT Authentication and Authorization
        authn_policy = JWTAuthenticationPolicy()
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        config.add_request_method(get_user, name='user', reify=True)

        # Preflight OPTIONS route
        config.add_route('cors_preflight', '/{catch_all:.*}', request_method='OPTIONS')

        config.scan('runlog_backend.views')

        return config.make_wsgi_app()
