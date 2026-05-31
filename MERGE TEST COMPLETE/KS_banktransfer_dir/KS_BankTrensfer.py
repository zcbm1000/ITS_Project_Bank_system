from datetime import datetime
from config import config
from dataBase import userDb
from dataBase import accountDb as accdb

# [수정 전] 단독 실행 목적의 임시 db 딕셔너리와 예금주 테스트 고정값을 파일 내부에 들고 있어 전체 시스템과 연동되지 않음
# [수정 후] 자체 db 변수를 완전히 걷어내고, 공용 회원 창고인 dataBase.userDb.users를 검색하도록 순회 연동함
# [왜 이렇게 해야 하는가] 로그인한 회원의 실제 실시간 세션 정보 및 수경이 구현한 회원 데이터베이스와 100% 결합하기 위함
def accountTransfer(cur_u):
    target_id = input("이체할 상대방 계좌번호: ").strip()

    target_user = None
    for u_id, u_obj in userDb.users.items():
        if u_obj.userAccount == target_id:
            target_user = u_obj
            break

    if target_user is None:
        print("에러: 존재하지 않는 계좌번호입니다.")
        return

    if target_id == cur_u.userAccount:
        print("에러: 본인 계좌로의 이체는 불가능합니다.")
        return

    print(f"\n조회 결과: {target_user.userName}님")
    confirm_name = input("예금주가 맞습니까? (1.예 / 2.아니오): ").strip()

    if confirm_name != '1':
        print("이체를 취소합니다.")
        return

    try:
        amt = int(input("이체할 금액: "))

        if amt <= 0:
            print("에러: 0원 이하의 금액은 입력할 수 없습니다.")
            return

        my_balance = accdb.get_balance(cur_u.userAccount)
        if my_balance is None or amt > my_balance:
            print(f"에러: 잔액이 부족합니다. (현재 잔액: {my_balance}원)")
            return

        print(f"\n--- [이체 확인] ---")
        print(f"수신: {target_user.userName}")
        print(f"금액: {amt}원")
        final_check = input("정말 이체하시겠습니까? (1.승인 / 2.취소): ").strip()

        if final_check == '1':
            accdb.accounts[cur_u.userAccount]['balance'] -= amt
            accdb.accounts[target_id]['balance'] += amt

            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            if 'history' not in accdb.accounts[cur_u.userAccount]:
                accdb.accounts[cur_u.userAccount]['history'] = []
            if 'history' not in accdb.accounts[target_id]:
                accdb.accounts[target_id]['history'] = []

            accdb.accounts[cur_u.userAccount]['history'].append({
                "time": now, "type": "출금(이체)", "target": target_user.userName, "amt": amt
            })
            accdb.accounts[target_id]['history'].append({
                "time": now, "type": "입금(이체)", "target": cur_u.userName, "amt": amt
            })

            accdb.save_db()
            print(f"이체 완료! (잔액: {accdb.get_balance(cur_u.userAccount)}원)")
        else:
            print("이체가 중단되었습니다.")

    except ValueError:
        print("에러: 숫자만 입력 가능합니다.")

def bankMain(cur_u):
    while True:
        my_balance = accdb.get_balance(cur_u.userAccount)
        print("\n" + "="*35)
        print(f" [ 대전뱅크 ]  접속자: {cur_u.userName}")
        print(f" 현재 잔액: {my_balance}원")
        print("="*35)
        print("1. 계좌 이체")
        print("2. 거래 내역")
        print("3. 종료")

        choice = input("선택: ").strip()

        if choice == config.BANK_TRANSFER:
            accountTransfer(cur_u)
        elif choice == config.BANK_HISTORY:
            print(f"\n--- [{cur_u.userName}님 내역] ---")
            if 'history' not in accdb.accounts[cur_u.userAccount] or not accdb.accounts[cur_u.userAccount]['history']:
                print("거래 내역이 없습니다.")
            else:
                for log in accdb.accounts[cur_u.userAccount]['history']:
                    print(f"[{log['time']}] {log['type']} | {log['target']} | {log['amt']}원")
        elif choice == config.BANK_EXIT:
            break
        else:
            print("잘못된 입력입니다.")