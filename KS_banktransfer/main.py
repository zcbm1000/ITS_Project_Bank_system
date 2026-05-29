from datetime import datetime


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
    print("--- [시스템] 데이터가 저장되었습니다. ---")


def accountTransfer():
    target_id = input("이체할 상대방 계좌: ")
    if target_id not in db or db[target_id].userAccount is None:
        print("대상을 찾을 수 없거나 계좌가 없습니다.")
        return
    
    print(f"받으실 분: {db[target_id].userName}님이 맞습니까?")
    if input("1.맞음 2.취소: ") != '1': return

    try:
        amt = int(input("이체 금액: "))
        if amt > cur_u.userAccount['balanceCheck']:
            print("잔액 부족!")
            return
        
        cur_u.userAccount['balanceCheck'] -= amt
        db[target_id].userAccount['balanceCheck'] += amt
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        cur_u.userAccount['history'].append({"type":"출금", "amt":amt, "target":db[target_id].userName, "time":now})
        db[target_id].userAccount['history'].append({"type":"입금", "amt":amt, "target":cur_u.userName, "time":now})
        
        save_db(db) 
        print("이체 완료!")
    except ValueError:
        print("숫자만 입력 가능합니다.")


def main():
    while True:
        print("\n" + "="*30)
        print(f" [ 대전뱅크 ]  접속 중: {cur_u.userName}님")
        print(f" 현재 잔액: {cur_u.userAccount['balanceCheck']}원")
        print("="*30)
        print("1. 계좌 이체\n2. 거래 내역 확인\n3. 종료")
        
        choice = input("입력: ")
        if choice == '1': accountTransfer()
        elif choice == '2':
            for log in cur_u.userAccount['history']:
                print(f"[{log['time']}] {log['type']} | {log['target']} | {log['amt']}원")
        elif choice == '3': break

if __name__ == "__main__":
    main()