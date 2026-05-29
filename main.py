from datetime import datetime
import config            
import dataBase
import accdb

now = datetime.now()
print(f'now')

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

def signUp():
    userId = input("사용할 아이디 입력: ")
    if userId in db:
        return
    userPw = input("비밀번호 입력: ")
    userName = input("이름 입력: ")
    userMail = input("메일 주소 입력: ")
    userPhone = input("전화번호 입력 (ex: 010-1234-5678): ")
    db[userId] = UserInfo(userName, userPw, userMail, userPhone)
    save_db(db)

def signIn():
    global cur_u
    userId = input("아이디: ")
    userPw = input("비밀번호: ")
    if userId in db and db[userId].userPw == userPw:
        cur_u = db[userId]
        cur_u.userId = userId 
    else:
        print(config.MSG.get("FAIL_AUTH", "인증 실패"))

def findId():
    name = input("이름 입력: ")
    phone = input("전화번호 입력: ")
    found_id = None
    for userId, user_obj in db.items():
        if user_obj.userName == name and user_obj.userPhone == phone:
            found_id = userId
            break
    if found_id:
        print(f"[{found_id}]")

def findPw():
    userId = input("아이디 입력: ")
    if userId not in db:
        return
    name = input("이름 입력: ")
    mail = input("메일 주소 입력: ")
    user = db[userId]
    if user.userName == name and user.userMail == mail:
        print(f"[{user.userPw}]")

def main():
    global cur_u
    while True:
        if cur_u is None:
            sel = input("1.가입 2.로그인 3.ID찾기 4.PW찾기 0.종료: ")
            if sel == '1': signUp()
            elif sel == '2': signIn()
            elif sel == '3': findId()
            elif sel == '4': findPw()
            elif sel == '0':
                save_db(db)
                break
        else:
            sel = input("1.계좌 2.메모 3.할일 4.정보 5.로그아웃 0.종료: ")
            if sel == '1': pass
            elif sel == '2': pass
            elif sel == '3': pass
            elif sel == '4': pass
            elif sel == '5': cur_u = None
            elif sel == '0':
                save_db(db)
                break

def accountMenu():
    while True:
        choice = int(input("1.신규생성 0.뒤로가기: "))
        if choice == config.CREATENEWACCOUNT:
            createAccount()
        elif choice == config.BACKTOMAINMENU:
            break

def createAccount():
    while True:
        account = input("계좌 번호(13자리): ")
        if len(account) != 13:
            continue
        if account in accountDb.accounts:
            continue
        accountDb.accounts[account] = {"balance": 0}
        return 




def bank_process():
    accdb.load_db()
    userId = input('ID: ')
    userPw = input('PW: ')
    if userId != config.LOGIN_USER and userPw != config.LOGIN_USER:
        return
    
    while True:
        menu = input('1.입금 2.출금 0.종료: ')
        if menu == '0':
            accdb.save_db()
            break

        acc_num = input('계좌번호: ')
        money = int(input('금액: '))

        if menu == config.MENU_DEPOSIT:
            accdb.deposit(acc_num, money)
        elif menu == config.MENU_WITHDRAW:
            accdb.withdraw(acc_num, money)            



class User:
    def __init__(self, userName, userAccount):
        self.userName = userName
        self.userAccount = userAccount

db = {
    "123-456": User("김철수", {"balanceCheck": 50000, "history": []}),
    "789-012": User("이영희", {"balanceCheck": 10000, "history": []}),
    "999-999": User("박지민", {"balanceCheck": 150000,"history": []})
}

cur_u = db["123-456"] 

def save_db(data):
    pass

def accountTransfer():
    target_id = input("상대방 계좌: ")
    if target_id not in db or db[target_id].userAccount is None:
        return
    
    if input("1.확인 2.취소: ") != '1': return

    try:
        amt = int(input("금액: "))
        if amt > cur_u.userAccount['balanceCheck']:
            return
        
        cur_u.userAccount['balanceCheck'] -= amt
        db[target_id].userAccount['balanceCheck'] += amt
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        cur_u.userAccount['history'].append({"type":"출금", "amt":amt, "target":db[target_id].userName, "time":now})
        db[target_id].userAccount['history'].append({"type":"입금", "amt":amt, "target":cur_u.userName, "time":now})
        save_db(db)
    except ValueError:
        pass

def bank_main():
    while True:
        choice = input("1.이체 2.내역 3.종료: ")
        if choice == '1': accountTransfer()
        elif choice == '2':
            for log in cur_u.userAccount['history']:
                print(f"[{log['time']}] {log['type']} | {log['target']} | {log['amt']}원")
        elif choice == '3': break