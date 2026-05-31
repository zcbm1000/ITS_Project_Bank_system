# ==========================================================
# sg_mainMenu/database.py
# 역할: 회원 데이터를 json 파일에 저장하고 불러오는 함수 모음
# ==========================================================

import json
from config import config
from dataBase import userDb

# [수정 전 - save_db]
# def save_db(db_data):              ← db 딕셔너리를 인자로 받았음
#     for userId, userInfo in db_data.items():
#         ...
#         "managementMust": [vars(t) for t in userInfo.managementMust]
#                            ↑ Todo 객체를 vars()로 딕셔너리 변환했음
#
# [수정 후 - save_db]
# def save_db():                     ← 인자 없음. userDb.users 를 직접 씀
#     for userId, userInfo in userDb.users.items():
#         ...
#         "managementMust": userInfo.managementMust
#                            ↑ mustFinal 에서 이미 딕셔너리로 저장하므로 그대로 씀
#
# [왜 이렇게 해야 하는가]
# 기존 save_db 는 Todo 객체를 vars()로 변환해서 저장했는데
# mustFinal.py 에서는 must 항목을 처음부터 딕셔너리로 저장함.
# 저장 방식이 달라서 load 할 때 구조가 깨지는 문제가 있었음.
# 또한 인자로 db 를 넘기는 방식은 userDb 를 쓰는 구조와 맞지 않음.
# save_db() 가 userDb.users 를 직접 참조하면 어디서 호출하든 동일하게 동작함.

def save_db():
    serialized = {}
    for userId, userInfo in userDb.users.items():
        serialized[userId] = {
            "userName":       userInfo.userName,
            "userPw":         userInfo.userPw,
            "userMail":       userInfo.userMail,
            "userPhone":      userInfo.userPhone,
            "userAccount":    userInfo.userAccount,
            "managementMemo": userInfo.managementMemo,
            "managementMust": userInfo.managementMust
        }
    with open(config.DB_FILE, "w", encoding="utf-8") as f:
        json.dump(serialized, f, ensure_ascii=False, indent=4)


# [수정 전 - load_db]
# def load_db(UserClass, TodoClass):
#     if not os.path.exists(config.DB_FILE):   ← os 모듈 사용
#         return {}                             ← 반환값 있었음
#     ...
#     for t_data in info['managementMust']:
#         todo = TodoClass(t_data['tit'], t_data['exp'])  ← Todo 객체로 복구
#         todo.mustComplete = t_data['mustComplete']
#         userInfo.managementMust.append(todo)
#     recovered[userId] = userInfo
#     return recovered                          ← 반환값 있었음
#
# [수정 후 - load_db]
# os 제거 → try/except FileNotFoundError 로 대체
# Todo 객체 복구 제거 → 딕셔너리 그대로 담음
# return 제거 → userDb.users 에 직접 담음
#
# [왜 이렇게 해야 하는가]
# os 는 배우지 않은 모듈이고 try/except 로 완전히 대체 가능함.
# mustFinal 이 must 항목을 딕셔너리로 저장하므로
# load 할 때도 딕셔너리 그대로 담아야 저장/불러오기 방식이 일치함.
# return 대신 userDb.users 에 직접 담으면
# 어느 파일에서 load_db 를 호출해도 userDb.users 에서 데이터를 꺼낼 수 있음.

def load_db(UserClass, TodoClass):
    try:
        with open(config.DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for userId, info in data.items():
                userInfo = UserClass(
                    info['userName'],
                    info['userPw'],
                    info['userMail'],
                    info['userPhone']
                )
                userInfo.userAccount    = info.get('userAccount', None)
                userInfo.managementMemo = info.get('managementMemo', [])
                userInfo.managementMust = info.get('managementMust', [])
                userDb.users[userId] = userInfo
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}")
