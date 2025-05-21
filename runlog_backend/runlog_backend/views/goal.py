from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPNoContent, HTTPForbidden
from runlog_backend.models.meta import DBSession
from runlog_backend.models.models import Goal, User
import jwt

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
# Tambah target
@view_config(route_name='create_goal', request_method='POST', renderer='json')
def create_goal(request):
    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")
    data = request.json_body

    month = data.get('month')
    target_distance = data.get('target_distance')

    if not month or not target_distance:
        return {'error': 'month dan target_distance wajib diisi'}, 400

    goal = Goal(
        user_id=user.id,
        month=month,
        target_distance=target_distance
    )
    DBSession.add(goal)
    DBSession.commit()  # commit supaya permanen

    return {'message': 'Target berhasil ditambahkan.'}

# Update target
@view_config(route_name='update_goal', request_method='PUT', renderer='json')
def update_goal(request):
    user = request.user
    if not user:
        raise HTTPForbidden("Token tidak valid")
    goal_id = int(request.matchdict['id'])
    data = request.json_body

    goal = DBSession.query(Goal).filter_by(id=goal_id, user_id=user.id).first()
    if not goal:
        raise HTTPNotFound("Target tidak ditemukan.")

    goal.month = data.get('month', goal.month)
    goal.target_distance = data.get('target_distance', goal.target_distance)
    DBSession.commit()  # commit supaya update tersimpan

    return {'message': 'Target berhasil diperbarui.'}


# Lihat semua target
@view_config(route_name='get_goals', request_method='GET', renderer='json')
def get_goals(request):
    try:
        user = get_user_from_request(request)
    except HTTPForbidden as e:
        return HTTPForbidden(str(e))

    goals = (
        DBSession.query(Goal)
        .filter_by(user_id=user.id)
        .order_by(Goal.month.asc())
        .all()
    )

    return [
        {
            'id': goal.id,
            'month': goal.month,
            'target_distance': goal.target_distance
        }
        for goal in goals
    ]
 

# Hapus target
@view_config(route_name='delete_goal', request_method='DELETE', renderer='json')
def delete_goal(request):
    user = getattr(request, 'user', None)
    if not user:
        raise HTTPForbidden("Token tidak valid")
    goal_id = int(request.matchdict.get('id', 0))
    if goal_id == 0:
        raise HTTPNotFound("ID target tidak ditemukan.")

    goal = DBSession.query(Goal).filter_by(id=goal_id, user_id=user.id).first()
    if not goal:
        raise HTTPNotFound("Target tidak ditemukan.")

    DBSession.delete(goal)
    DBSession.commit()
    return HTTPNoContent()