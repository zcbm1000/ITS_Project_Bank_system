# database.py
import json
import os
import config

def save_db(db_data):
    serialized = {}
    for u_id, user in db_data.items():
        serialized[u_id] = {
            "userName": user.userName,
            "u_pw": user.u_pw,
            "userMail": user.userMail,
            "userPhone": user.userPhone,
            "userAccount": user.userAccount, # {"balanceCheck": 0, "history": []}
            "managementMemo": user.managementMemo,
            "managementMust": user.managementMust # 리스트 형태
        }
    with open(config.DB_FILE, "w", encoding="utf-8") as f:
        json.dump(serialized, f, ensure_ascii=False, indent=4)

def load_db(UserClass):
    if not os.path.exists(config.DB_FILE): return {}
    try:
        with open(config.DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            recovered = {}
            for userId, info in data.items():
                user = UserClass(info['userName'], info['userPw'], info['userMail'], info['userPhone'])
                user.userAccount = info['userAccount']
                user.managementMemo = info['managementMemo']
                user.managementMust = info['managementMust']
                recovered[userId] = user
            return recovered
    except: return {}