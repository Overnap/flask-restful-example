from api import UserApi
from api import AuthApi
from api import RoomApi
from api import RoomAllApi


def initialize(api):
    api.add_resource(UserApi, '/user')
    api.add_resource(AuthApi, '/auth')
    api.add_resource(RoomApi, '/room')
    api.add_resource(RoomAllApi, '/room/all')
    # TODO: GET /room으로 전체 정보 얻고 GET room/id로 방 정보 얻는 구조가 더 좋겠다
