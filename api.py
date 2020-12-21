from flask_restful import Resource, reqparse
from database import db
import models
import re
import json
import jwt


class UserApi(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            # check validation
            if not re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', args['email']):
                return {'Error': 'email is invalid'}, 400
            if models.User.query.filter_by(email=args['email']).first() is not None:
                return {'Error': 'email already exists'}, 400
            if models.User.query.filter_by(username=args['username']).first() is not None:
                return {'Error': 'username already exists'}, 400
            if len(args['password']) < 8:
                return {'Error': 'password is too short'}, 400

            user = models.User(**args)
            db.session.add(user)
            db.session.commit()
            return {'success': True}, 201
        except Exception as e:
            print(e)
            return {'Error': str(e)}, 400


class AuthApi(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            user = models.User.query.filter_by(email=args['email']).first()
            # email existence test
            if user is None:
                return {'Error': 'data incorrect'}, 400
            # password test
            if not user.check_password(args['password']):
                return {'Error': 'data incorrect'}, 400
            # login succeed
            # TODO: token or session?
            return {'success': True, 'username': user.username}, 200
        except Exception as e:
            print(e)
            return {'Error': str(e)}, 400

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('access-token', location='headers')
            args = parser.parse_args()
            # TODO: 토큰 비교하고 시간 너무 오래됏으면 재발급 ㄴㄴ
        except Exception as e:
            return {'Error': str(e)}, 400

    def delete(self):
        try:
            # TODO: 로그아웃; 토큰 블랙리스트
            return
        except Exception as e:
            return {'Error': str(e)}, 400


class RoomApi(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('uploader', type=str)
            parser.add_argument('address', type=str)
            parser.add_argument('contact', type=str)
            parser.add_argument('introduction', type=str)
            parser.add_argument('latitude', type=float)
            parser.add_argument('longitude', type=float)
            args = parser.parse_args()

            if args['uploader'] is None or not args['uploader']:
                return {'Error': 'null data is not allowed'}, 400
            if args['address'] is None or not args['address']:
                return {'Error': 'null data is not allowed'}, 400
            if args['contact'] is None or not args['contact']:
                return {'Error': 'null data is not allowed'}, 400
            if args['latitude'] is None:
                return {'Error': 'null data is not allowed'}, 400
            if args['longitude'] is None:
                return {'Error': 'null data is not allowed'}, 400
            if args['introduction'] is None:
                args['introduction'] = ' '

            room = models.Room(**args)
            db.session.add(room)
            db.session.commit()
            return {'success': True}, 200
        except Exception as e:
            print(e)
            return {'Error': str(e)}, 400

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('json', type=json.loads)
            args = parser.parse_args()
            # TODO: 당연히 안좋은 방식 통짜 json이 아니라 따로따로 오도록 만들자
            args = args['json']

            room = models.Room.query.filter_by(id=args['id']).first()
            return {
                'uploader': room.uploader,
                'address': room.address,
                'contact': room.contact,
                'introduction': room.introduction,
                'latitude': room.latitude,
                'longitude': room.longitude
            }, 200
        except Exception as e:
            print(e)
            return {'Error': str(e)}, 400

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            args = parser.parse_args()

            models.Room.query.filter_by(id=args['id']).first().delete()
            db.session.commit()
            # TODO: 작동 확인 필요
            return {'success': True}, 200
        except Exception as e:
            print(e)
            return {'Error': str(e)}, 400


class RoomAllApi(Resource):
    def get(self):
        try:
            rooms = models.Room.query.order_by(models.Room.id).all()
            result = []
            for room in rooms:
                result.append({
                    'id': room.id,
                    'address': room.address,
                    'latitude': room.latitude,
                    'longitude': room.longitude
                })
            return {'rooms': result}, 200
        except Exception as e:
            print(e)
            return {'Error': str(e)}, 400
