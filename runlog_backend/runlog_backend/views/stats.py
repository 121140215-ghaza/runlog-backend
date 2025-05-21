from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden
from runlog_backend.models.meta import DBSession
from runlog_backend.models.models import RunLog, User
import jwt
from sqlalchemy.sql import func
from datetime import datetime

SECRET_KEY = 'supersecretkey123'

def get_user_from_request(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPForbidden("Token tidak ditemukan")

    try:
        token = auth_header.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
        user = DBSession.query(User).get(user_id)
        if not user:
            raise HTTPForbidden("User tidak valid")
        return user
    except Exception:
        raise HTTPForbidden("Token invalid")

@view_config(route_name='get_stats', request_method='GET', renderer='json')
def get_stats(request):
    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")

    runs = DBSession.query(RunLog).filter_by(user_id=user.id).all()
    if not runs:
        return {
            'total_distance': 0,
            'total_duration': 0,
            'avg_distance': 0,
            'avg_duration': 0
        }

    total_distance = sum(run.distance for run in runs)
    total_duration = sum(run.duration for run in runs)
    count = len(runs)

    return {
        'total_distance': round(total_distance, 2),
        'total_duration': int(total_duration),
        'avg_distance': round(total_distance / count, 2),
        'avg_duration': round(total_duration / count, 2)
    }
