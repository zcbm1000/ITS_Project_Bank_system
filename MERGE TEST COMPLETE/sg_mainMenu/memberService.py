from config import config
from dataBase import userDb
from sg_mainMenu import database


# [수정 전 - 클래스 위치]
# UserInfo, Todo 클래스가 main.py 안에 있었음.
#
# [수정 후]
# memberService.py 로 분리.
#
# [왜 이렇게 해야 하는가]
# 클래스 정의는 데이터 구조를 담당하므로
# 회원 관련 로직을 모아둔 memberService 에 있는 게 구조상 자연스러움.
# database.py 가 load_db 에서 UserClass 를 받아 객체를 만들기 때문에
# 클래스 정의가 memberService 에 있어야 import 구조가 꼬이지 않음.

class Todo:
    def __init__(self, tit, exp):
        self.tit = tit
        self.exp = exp
        self.mustComplete = False

class UserInfo:
    def __init__(self, userName, userPw, userMail, userPhone):
        self.userName       = userName
        self.userPw         = userPw
        self.userMail       = userMail
        self.userPhone      = userPhone
        self.userAccount    = None
        self.managementMemo = []
        self.managementMust = []


# [수정 전]
# db = load_db(UserInfo, Todo)   ← 자체 db 딕셔너리를 반환값으로 받아 관리
#
# [수정 후]
# database.load_db(UserInfo, Todo)  ← 반환값 없음. userDb.users 에 자동으로 담김
#
# [왜 이렇게 해야 하는가]
# 기존에는 memberService 가 자체 'db' 딕셔너리를 만들어서
# mainMenu 에서 'database.save_db(memberService.db)' 처럼 인자로 넘겨야 했음.
# userDb.users 를 직접 쓰면 어느 파일에서든 같은 데이터에 접근 가능하고
# 인자를 주고받을 필요가 없어짐.

database.load_db(UserInfo, Todo)


def signUp():
    print("\n--- [회원 가입 (signUp)] ---")
    userId = input("사용할 아이디 입력: ")

    # [수정 전] if userId in db:
    # [수정 후] if userId in userDb.users:
    # db 딕셔너리 대신 userDb.users 를 직접 참조.
    if userId in userDb.users:
        print("에러: 이미 존재하는 아이디입니다.")
        return

    userPw    = input("비밀번호 입력: ")
    userName  = input("이름 입력: ")
    userMail  = input("메일 주소 입력: ")
    userPhone = input("전화번호 입력 (ex: 010-1234-5678): ")

    # [수정 전] db[userId] = UserInfo(...)
    # [수정 후] userDb.users[userId] = UserInfo(...)
    userDb.users[userId] = UserInfo(userName, userPw, userMail, userPhone)

    # [수정 전] save_db(db)   ← db 인자 전달
    # [수정 후] database.save_db()  ← 인자 없음
    database.save_db()
    print(f"\n축하합니다, {userName}님! 회원가입이 완료되었습니다.")


def signIn():
    # [수정 전]
    # def signIn():
    #     global cur_u          ← 함수 안에서 전역변수를 직접 바꿈
    #     ...
    #     cur_u = db[userId]    ← mainMenu 의 cur_u 를 몰래 변경
    #     (return 없음)
    #
    # [수정 후]
    # global cur_u 제거.
    # 로그인 성공 → return cur_u  (mainMenu 에서 받아서 관리)
    # 로그인 실패 → return None   (mainMenu 의 cur_u 가 None 유지)
    #
    # [왜 이렇게 해야 하는가]
    # global 변수를 여러 함수에서 직접 바꾸면
    # cur_u 가 언제 어디서 바뀌었는지 추적하기 어려움.
    # cur_u 는 mainMenu 한 곳에서만 관리하는 게 구조상 명확함.
    # return 값으로 받으면 mainMenu 에서 'cur_u = memberService.signIn()' 한 줄로 처리됨.

    print("\n--- [로그 인 (signIn)] ---")
    userId = input("아이디: ")
    userPw = input("비밀번호: ")

    if userId in userDb.users and userDb.users[userId].userPw == userPw:
        cur_u = userDb.users[userId]
        cur_u.userId = userId
        print(f"\n로그인 성공! {cur_u.userName}님 환영합니다.")
        return cur_u
    else:
        print("\n에러: " + config.MSG.get("FAIL_AUTH", "인증 실패"))
        return None


def findId():
    print("\n--- [아이디 찾기 (findId)] ---")
    userName  = input("이름 입력: ")
    userPhone = input("전화번호 입력: ")

    found_id = None

    # [수정 전] for userId, user_obj in db.items():
    # [수정 후] for userId, user_obj in userDb.users.items():
    for userId, user_obj in userDb.users.items():
        if user_obj.userName == userName and user_obj.userPhone == userPhone:
            found_id = userId
            break

    if found_id:
        print(f"\n조회 결과: [{found_id}] 입니다.")
    else:
        print("\n에러: 일치하는 사용자 정보가 없습니다.")


def findPw():
    print("\n--- [비밀번호 찾기 (findPw)] ---")
    userId = input("아이디 입력: ")

    # [수정 전] if userId not in db:
    # [수정 후] if userId not in userDb.users:
    if userId not in userDb.users:
        print("\n에러: 존재하지 않는 아이디입니다.")
        return

    userName = input("이름 입력: ")
    userMail = input("메일 주소 입력: ")

    # [수정 전] user = db[userId]
    # [수정 후] user = userDb.users[userId]
    user = userDb.users[userId]
    if user.userName == userName and user.userMail == userMail:
        print(f"\n조회 결과: [{userId}] 님의 비밀번호는 [{user.userPw}] 입니다.")
    else:
        print("\n에러: 입력하신 정보가 일치하지 않습니다.")
