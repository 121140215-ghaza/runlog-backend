from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')              # kalau pakai Jinja2 templating
        config.include('runlog_backend.routes')       # load route dari routes.py
        config.include('runlog_backend.models')       # inisialisasi DBSession & engine
        config.scan('runlog_backend.views')            
        return config.make_wsgi_app()
         