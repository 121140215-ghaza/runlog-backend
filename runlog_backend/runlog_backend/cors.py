from pyramid.response import Response

def cors_tween_factory(handler, registry):
    def cors_tween(request):
        allowed_origin = 'http://localhost:5173'
        origin = request.headers.get('Origin')

        if request.method == 'OPTIONS':
            response = Response()
            if origin and allowed_origin in origin:
                response.headers.update({
                    'Access-Control-Allow-Origin': allowed_origin,
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                })
            response.status_code = 204
            return response

        response = handler(request)
        if origin and allowed_origin in origin:
            response.headers.update({
                'Access-Control-Allow-Origin': allowed_origin,
                'Access-Control-Allow-Credentials': 'true',
                'Vary': 'Origin',
            })
        return response

    return cors_tween

# ⬇⬇⬇ jangan lupa ini bro
def includeme(config):
    config.add_tween('runlog_backend.cors.cors_tween_factory')
