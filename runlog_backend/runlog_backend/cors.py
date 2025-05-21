def cors_tween_factory(handler, registry):
    def cors_tween(request):
        allowed_origin = 'http://localhost:5173'
        origin = request.headers.get('Origin')

        if request.method == 'OPTIONS':
            response = request.response
            if origin == allowed_origin:
                response.headers['Access-Control-Allow-Origin'] = allowed_origin
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.status_code = 204
            return response

        response = handler(request)
        if origin == allowed_origin:
            response.headers['Access-Control-Allow-Origin'] = allowed_origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            # optional: bisa tambahin ini biar browser gak complain
            response.headers['Vary'] = 'Origin'

        return response

    return cors_tween
