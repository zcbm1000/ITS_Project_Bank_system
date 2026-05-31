from datetime import datetime
import config            
from database import save_db, load_db
from ITS_Project_Bank_system import main


class Todo:
    def __init__(self, tit, exp):
        self.tit = tit
        self.exp = exp
        self.mustComplete = False 

class UserInfo:
    def __init__(self, userName, userPw, userMail, userPhone):
        self.userName = userName
        self.userPw = userPw
        self.userMail = userMail
        self.userPhone = userPhone
        self.userAccount = None
        self.managementMemo = []
        self.managementMust = []


db = load_db(UserInfo, Todo) 
cur_u = None             

# 1. 회원 가입 (signUp)
def signUp():
    print("\n--- [회원 가입 (signUp)] ---")
    userId = input("사용할 아이디 입력: ")
    
    if userId in db:
        print("에러: 이미 존재하는 아이디입니다.")
        return

    userPw = input("비밀번호 입력: ")
    userName = input("이름 입력: ")
    userMail = input("메일 주소 입력: ")
    userPhone = input("전화번호 입력 (ex: 010-1234-5678): ")

    db[userId] = UserInfo(userName, userPw, userMail, userPhone)
    save_db(db)
    print(f"\n축하합니다, {userName}님! 회원가입이 완료되었습니다.")

# 2. 로그 인 (signIn)
def signIn():
    global cur_u
    print("\n--- [로그 인 (signIn)] ---")
    userId = input("아이디: ")
    userPw = input("비밀번호: ")

    if userId in db and db[userId].userPw == userPw:
        cur_u = db[userId]
        cur_u.userId = userId 
        print(f"\n로그인 성공! {cur_u.userName}님 환영합니다.")
    else:
        print("\n에러: " + config.MSG.get("FAIL_AUTH", "인증 실패"))

# 3. 아이디 찾기 (findId)
def findId():
    print("\n--- [아이디 찾기 (findId)] ---")
    name = input("이름 입력: ")
    phone = input("전화번호 입력: ")

    found_id = None
    for userId, user_obj in db.items():
        
        if user_obj.userName == name and user_obj.userPhone == phone:
            found_id = userId
            break

    if found_id:
        print(f"\n조회 결과: [{found_id}] 입니다.")
    else:
        print("\n에러: 일치하는 사용자 정보가 없습니다.")

# 4. 비밀번호 찾기 (findPw)
def findPw():
    print("\n--- [비밀번호 찾기 (findPw)] ---")
    userId = input("아이디 입력: ")
    
    if userId not in db:
        print("\n에러: 존재하지 않는 아이디입니다.")
        return

    name = input("이름 입력: ")
    mail = input("메일 주소 입력: ")

    user = db[userId]
    if user.userName == name and user.userMail == mail:
        print(f"\n조회 결과: [{userId}] 님의 비밀번호는 [{user.userPw}] 입니다.")
    else:
        print("\n에러: 입력하신 정보가 일치하지 않습니다.")

if __name__ == "__main__":
    main()
