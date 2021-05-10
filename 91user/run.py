from user import User, ClientSqlite
from config.uids import USERS_UID
import json

db = ClientSqlite()


def fetchall_table(uid):
    sql = '''SELECT data FROM users WHERE uid = ('{}')'''.format(uid)
    result = db.fetchall_table(sql)
    if result != None:
        result = result[0]
        data = json.loads(result[0])
        data_num = len(data)
        return {'data': data, 'data_num': int(data_num)}
    else:
        return None

def insert_table(data):
    uid = data['uid']
    name = data['name']
    videos = json.dumps(data['data'])
    sql = '''INSERT INTO users(uid, name,data) VALUES('{0}','{1}','{2}')'''.format(uid, name, videos)
    db.insert_update_table(sql)

def update_table(data):
    uid = data['uid']
    name = data['name']
    videos = json.dumps(data['data'])
    sql = '''UPDATE users SET data = ('{0}') WHERE uid = "{1}"'''.format(videos, uid)
    db.insert_update_table(sql)



if __name__ == "__main__":
    for i in USERS_UID:
        user = User(i)
        public_data = user.public_data()
        public_num = public_data['public_video']
        local_data = fetchall_table(i)
        if local_data != None and public_num > local_data['data_num']:
            # if public_num > local_data['data_num']
            user_data = user.parse_video()
            update_table(user_data)
            print('数据更新.....\n')
        elif  local_data != None and public_num == local_data['data_num']:
            print('公开视频与本地数据相符')
            pass
        else:
            user_data = user.parse_video()
            insert_table(user_data)
            print('数据新增.....\n')
    db.close_conn()