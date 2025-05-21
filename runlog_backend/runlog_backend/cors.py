def cors_tween_factory(handler, registry):
    def cors_tween(request):
        if request.method == 'OPTIONS':
            # response untuk preflight
            response = request.response
            origin = request.headers.get('Origin')
            allowed_origin = 'http://localhost:5173'
            if origin == allowed_origin:
                response.headers['Access-Control-Allow-Origin'] = allowed_origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

        response = handler(request)
        origin = request.headers.get('Origin')
        allowed_origin = 'http://localhost:5173'
        if origin == allowed_origin:
            response.headers['Access-Control-Allow-Origin'] = allowed_origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    return cors_tween
