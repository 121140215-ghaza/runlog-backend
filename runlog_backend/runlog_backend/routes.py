def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/') 
    config.add_route('register', '/api/register')
    config.add_route('login', '/api/login') 
    config.add_route('create_runlog', '/api/create/runlogs')
    config.add_route('get_runlogs', '/api/cek/runlogs')
    config.add_route('update_runlog', '/api/update/runlogs/{id}')
    config.add_route('delete_runlog', '/api/delete/runlogs/{id}')
