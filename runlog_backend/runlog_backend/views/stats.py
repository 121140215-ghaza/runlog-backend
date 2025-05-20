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

    # Group by month (YYYY-MM)
    results = (
        DBSession.query(
            func.to_char(RunLog.date, 'YYYY-MM').label('month'),
            func.sum(RunLog.distance).label('total_distance'),
            func.sum(RunLog.duration).label('total_duration')
        )
        .filter(RunLog.user_id == user.id)
        .group_by(func.to_char(RunLog.date, 'YYYY-MM'))
        .order_by('month')
        .all()
    )

    return [
        {
            'month': row.month,
            'total_distance': float(row.total_distance),
            'total_duration': int(row.total_duration)
        }
        for row in results
    ]
