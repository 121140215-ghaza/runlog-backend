import jwt
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.httpexceptions import HTTPForbidden
from runlog_backend.models.meta import DBSession
from runlog_backend.models.models import User

SECRET_KEY = 'supersecretkey123'

class JWTAuthenticationPolicy(CallbackAuthenticationPolicy):
    def authenticated_userid(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        try:
            token = auth_header.split()[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload.get('id')
        except Exception:
            return None

    def effective_principals(self, request):
        principals = ['Everyone']
        user_id = self.authenticated_userid(request)
        if user_id:
            principals.append('Authenticated')
        return principals

def get_user(request):
    user_id = request.authenticated_userid
    if user_id:
        return DBSession.query(User).get(user_id)
    return None
