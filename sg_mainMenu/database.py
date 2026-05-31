import json
import os
import config  

def save_db(db_data):
    """메모리 상의 db 딕셔너리를 JSON 파일로 저장 (Serialization)"""
    serialized = {}
    for userId, userInfo in db_data.items():
        
        serialized[userId] = {
            "userName": userInfo.userName,
            "userPw": userInfo.userPw,
            "userMail": userInfo.userMail,
            "userPhone": userInfo.userPhone,
            "userAccount": userInfo.userAccount,
            "managementMemo": userInfo.managementMemo,
            
            "managementMust": [vars(t) for t in userInfo.managementMust]
        }
    
    with open(config.DB_FILE, "w", encoding="utf-8") as f:
        
        json.dump(serialized, f, ensure_ascii=False, indent=4)

def load_db(UserClass, TodoClass):
    """파일에서 데이터를 읽어와서 다시 User/Todo 객체로 복구 (Deserialization)"""
    if not os.path.exists(config.DB_FILE):
        return {} 
    
    try:
        with open(config.DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            recovered = {}
            for userId, info in data.items():
                
                userInfo = UserClass(info['userName'], info['userPw'], info['userMail'], info['userPhone'])
                userInfo.userAccount = info['userAccount']
                userInfo.managementMemo = info['managementMemo']
                
               
                for t_data in info['managementMust']:
                    todo = TodoClass(t_data['tit'], t_data['exp'])
                    todo.mustComplete = t_data['mustComplete']
                    userInfo.managementMust.append(todo)
                
                recovered[userId] = userInfo
            return recovered
    except Exception as e:
        print(f"데이터 로드 중 오류 발생: {e}")
        return {}