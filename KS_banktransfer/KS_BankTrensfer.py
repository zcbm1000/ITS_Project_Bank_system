from datetime import datetime

class User:
    def __init__(self, userName, userAccount):
        self.userName = userName
        self.userAccount = userAccount

db = {
    "123-456": User("김철수", {"balanceCheck": 50000, "history": []}),
    "789-012": User("이영희", {"balanceCheck": 10000, "history": []}),
    "999-999": User("박지민", {"balanceCheck": 150000, "history": []})
}

cur_u = db["123-456"]

def save_db(data):
    print("\n--- [시스템] 데이터가 저장되었습니다. ---")

def accountTransfer():
    target_id = input("이체할 상대방 계좌번호: ")

    if target_id not in db:
        print("에러: 존재하지 않는 계좌번호입니다.")
        return

    if target_id == "123-456":
        print("에러: 본인 계좌로의 이체는 불가능합니다.")
        return

    target_user = db[target_id]
    print(f"\n조회 결과: {target_user.userName}님")
    confirm_name = input("예금주가 맞습니까? (1.예 / 2.아니오): ")

    if confirm_name != '1':
        print("이체를 취소합니다.")
        return

    try:
        amt = int(input("이체할 금액: "))

        if amt <= 0:
            print("에러: 0원 이하의 금액은 입력할 수 없습니다.")
            return

        if amt > cur_u.userAccount['balanceCheck']:
            print(f"에러: 잔액이 부족합니다. (현재 잔액: {cur_u.userAccount['balanceCheck']}원)")
            return
        print(f"\n--- [이체 확인] ---")
        print(f"수신: {target_user.userName}")
        print(f"금액: {amt}원")
        final_check = input("정말 이체하시겠습니까? (1.승인 / 2.취소): ")

        if final_check == '1':
            cur_u.userAccount['balanceCheck'] -= amt
            target_user.userAccount['balanceCheck'] += amt

            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            cur_u.userAccount['history'].append({
                "time": now, "type": "출금(이체)", "target": target_user.userName, "amt": amt
            })
            target_user.userAccount['history'].append({
                "time": now, "type": "입금(이체)", "target": cur_u.userName, "amt": amt
            })

            save_db(db)
            print(f"이체 완료! (잔액: {cur_u.userAccount['balanceCheck']}원)")
        else:
            print("이체가 중단되었습니다.")

    except ValueError:
        print("에러: 숫자만 입력 가능합니다.")

def main():
    while True:
        print("\n" + "="*35)
        print(f" [ 대전뱅크 ]  접속자: {cur_u.userName}")
        print(f" 현재 잔액: {cur_u.userAccount['balanceCheck']}원")
        print("="*35)
        print("1. 계좌 이체")
        print("2. 거래 내역")
        print("3. 종료")

        choice = input("선택: ")

        if choice == '1':
            accountTransfer()
        elif choice == '2':
            print(f"\n--- [{cur_u.userName}님 내역] ---")
            if not cur_u.userAccount['history']:
                print("거래 내역이 없습니다.")
            else:
                for log in cur_u.userAccount['history']:
                    print(f"[{log['time']}] {log['type']} | {log['target']} | {log['amt']}원")
        elif choice == '3':
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()