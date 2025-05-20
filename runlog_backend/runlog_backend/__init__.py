from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from runlog_backend.auth_policy import JWTAuthenticationPolicy, get_user

def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.include('runlog_backend.routes')
        config.include('runlog_backend.models')

        # Middleware JWT
        authn_policy = JWTAuthenticationPolicy()
        authz_policy = ACLAuthorizationPolicy()
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        config.add_request_method(get_user, name='user', reify=True) 

        config.scan('runlog_backend.views')

        return config.make_wsgi_app()
