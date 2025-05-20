import os
import jwt
import logging
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError 
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound, HTTPNoContent
from runlog_backend.models.models import RunLog, User
from runlog_backend.models.meta import DBSession

log = logging.getLogger(__name__)
SECRET_KEY = os.environ.get('JWT_SECRET', 'supersecretkey123')

def get_user_from_request(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPForbidden("Token tidak ditemukan")

    try:
        token = auth_header.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
        user = request.dbsession.get(User, user_id)
        if not user:
            raise HTTPForbidden("User tidak valid")
        return user

    except ExpiredSignatureError:
        raise HTTPForbidden("Token kadaluarsa")
    except InvalidTokenError:
        raise HTTPForbidden("Token tidak valid")
    except Exception as e:
        log.error(f"Token error: {e}")
        raise HTTPForbidden("Terjadi kesalahan saat verifikasi token")


@view_config(route_name='create_runlog', request_method='POST', renderer='json')
def create_runlog(request):
    if not request.content_type.startswith('application/json'):
        return {'error': 'Content-Type harus application/json'}

    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")
    data = request.json_body

    runlog = RunLog(
        user_id=user.id,
        date=data['date'],
        distance=data['distance'],
        duration=data['duration'],
        note=data.get('note')
    )

    request.dbsession.add(runlog)
    return {'message': 'Run log berhasil ditambahkan.'}


@view_config(route_name='get_runlogs', request_method='GET', renderer='json')
def get_runlogs(request):
    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")
    logs = request.dbsession.query(RunLog).filter_by(user_id=user.id).all()

    return [
        {
            'id': log.id,
            'date': log.date.isoformat(),
            'distance': log.distance,
            'duration': log.duration,
            'note': log.note
        }
        for log in logs
    ]

# Update log lari
@view_config(route_name='update_runlog', request_method='PUT', renderer='json')
def update_runlog(request):
    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")
    runlog_id = int(request.matchdict['id'])
    data = request.json_body

    log = DBSession.query(RunLog).filter_by(id=runlog_id, user_id=user.id).first()
    if not log:
        raise HTTPNotFound("Log tidak ditemukan.")

    log.date = data.get('date', log.date)
    log.distance = data.get('distance', log.distance)
    log.duration = data.get('duration', log.duration)
    log.note = data.get('note', log.note)

    return {'message': 'Log berhasil diperbarui.'}

# Hapus log lari
@view_config(route_name='delete_runlog', request_method='DELETE', renderer='json')
def delete_runlog(request):
    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")
    runlog_id = int(request.matchdict['id'])

    log = DBSession.query(RunLog).filter_by(id=runlog_id, user_id=user.id).first()
    if not log:
        raise HTTPNotFound("Log tidak ditemukan.")

    DBSession.delete(log)
    return HTTPNoContent()
