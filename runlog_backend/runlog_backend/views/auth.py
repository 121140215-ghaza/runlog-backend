import os
import jwt
import datetime
from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from runlog_backend.models.models import User

SECRET_KEY = os.environ.get('JWT_SECRET', 'supersecretkey123')  # pakai env kalau production

@view_config(route_name='register', request_method='POST', renderer='json')
def register(request):
    if not request.content_type.startswith('application/json'):
        return Response(json_body={'error': 'Content-Type harus application/json'}, status=400)

    data = request.json_body
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return Response(json_body={'error': 'Semua field wajib diisi.'}, status=400)

    hashed = bcrypt.hash(password)
    user = User(username=username, email=email, password=hashed)

    try:
        request.dbsession.add(user)
        request.dbsession.flush()
    except IntegrityError:
        return Response(json_body={'error': 'Username atau email sudah digunakan.'}, status=400)

    return {'message': 'User berhasil dibuat.'}


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    if not request.content_type.startswith('application/json'):
        return Response(json_body={'error': 'Content-Type harus application/json'}, status=400)

    data = request.json_body
    email = data.get('email')
    password = data.get('password')

    user = request.dbsession.query(User).filter_by(email=email).first()
    if not user or not bcrypt.verify(password, user.password):
        return Response(json_body={'error': 'Email atau password salah.'}, status=401)

    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return {'token': token}
