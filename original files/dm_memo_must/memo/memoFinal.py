import json
from config import config
from dataBase import memoDb
from datetime import datetime


# ==========================================================
# 저장 / 불러오기
# ==========================================================

MEMO_DB_PATH = 'memo_db.json'

def get_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def saveMemo():
    
    with open(MEMO_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(memoDb.memos, f, ensure_ascii=False, indent=2)


def loadMemo():
    
    try:
        with open(MEMO_DB_PATH, 'r', encoding='utf-8') as f:
            memoDb.memos = json.load(f)
    except FileNotFoundError:
        pass


def initUser(userId):
    
    if userId not in memoDb.memos:
        memoDb.memos[userId] = []


# ==========================================================
# 메모 관리 메뉴
# ==========================================================

def managementMemo(cur_u):
    userId = cur_u.userId
    loadMemo()          
    initUser(userId)    

    while True:
        print('\n[ 메모 관리 (managementMemo) ]')
        print(f'{config.MEMO_READ}.memoRead    {config.MEMO_WRITE}.memoWrite    {config.MEMO_UPDATE}.memoUpdate    {config.MEMO_DELETE}.memoDelete    {config.BACK}.back')
        choice = input('>> ')

        # ---------- memoRead ----------
        if choice == config.MEMO_READ:
            memos = memoDb.memos[userId]
            if not memos:
                print('작성된 메모가 없습니다.')
            else:
                print(f'\n[ 내 메모 목록 ] 총 {len(memos)}개 / 최대 {config.MAX_MEMO_COUNT}개')
                for memo in memos:
                    print(f"  ({memo['id']}) [{memo['title']}] {memo['content']}")
                    print(f"      작성: {memo['writeTime']}  |  수정: {memo['revisionTime']}")

        # ---------- memoWrite ----------
        elif choice == config.MEMO_WRITE:
            memos = memoDb.memos[userId]

            # 최대 개수 초과 체크
            if len(memos) >= config.MAX_MEMO_COUNT:
                print(f'메모는 최대 {config.MAX_MEMO_COUNT}개까지 작성할 수 있습니다.')
            else:
                # 제목 입력
                while True:
                    title = input(f'제목을 입력하세요 ({config.MAX_MEMO_TITLE_LENGTH}자 이하): ')
                    if len(title) > config.MAX_MEMO_TITLE_LENGTH:
                        print(f'{config.MAX_MEMO_TITLE_LENGTH}자를 초과했습니다. ({len(title)}자)')
                    elif len(title) == 0:
                        print('제목을 입력해주세요.')
                    else:
                        break

                # 내용 입력
                while True:
                    content = input(f'내용을 입력하세요 ({config.MAX_MEMO_LENGTH}자 이하): ')
                    if len(content) > config.MAX_MEMO_LENGTH:
                        print(f'{config.MAX_MEMO_LENGTH}자를 초과했습니다. ({len(content)}자)')
                    elif len(content) == 0:
                        print('내용을 입력해주세요.')
                    else:
                        break

                new_id = memos[-1]['id'] + 1 if memos else 1
                now = get_now()
                memos.append({
                    'id': new_id,
                    'title': title,
                    'content': content,
                    'writeTime': now,
                    'revisionTime': now
                })
                saveMemo()
                print(f'메모가 저장되었습니다. (id: {new_id})')

        # ---------- memoUpdate ----------
        elif choice == config.MEMO_UPDATE:
            memos = memoDb.memos[userId]
            if not memos:
                print('수정할 메모가 없습니다.')
            else:
                print('\n[ 수정할 메모 선택 ]')
                for memo in memos:
                    print(f"  ({memo['id']}) [{memo['title']}] {memo['content']}")

                try:
                    target_id = int(input('수정할 메모 번호: '))
                    target = None
                    for m in memos:
                        if m['id'] == target_id:
                            target = m
                            break

                    if target is None:
                        print('해당 번호의 메모가 없습니다.')
                    else:
                        # 제목 수정
                        while True:
                            new_title = input(f'새 제목 ({config.MAX_MEMO_TITLE_LENGTH}자 이하, 엔터 시 유지): ')
                            if new_title == '':
                                new_title = target['title']  # 엔터 치면 기존 유지
                                break
                            elif len(new_title) > config.MAX_MEMO_TITLE_LENGTH:
                                print(f'{config.MAX_MEMO_TITLE_LENGTH}자를 초과했습니다.')
                            else:
                                break

                        # 내용 수정
                        while True:
                            new_content = input(f'새 내용 ({config.MAX_MEMO_LENGTH}자 이하, 엔터 시 유지): ')
                            if new_content == '':
                                new_content = target['content']  # 엔터 치면 기존 유지
                                break
                            elif len(new_content) > config.MAX_MEMO_LENGTH:
                                print(f'{config.MAX_MEMO_LENGTH}자를 초과했습니다.')
                            else:
                                break

                        target['title'] = new_title
                        target['content'] = new_content
                        target['revisionTime'] = get_now()
                        saveMemo()
                        print('메모가 수정되었습니다.')

                except ValueError:
                    print('숫자를 입력하세요.')

        # ---------- memoDelete ----------
        elif choice == config.MEMO_DELETE:
            memos = memoDb.memos[userId]
            if not memos:
                print('삭제할 메모가 없습니다.')
            else:
                print('\n[ 삭제할 메모 선택 ]')
                for memo in memos:
                    print(f"  ({memo['id']}) [{memo['title']}] {memo['content']}")

                try:
                    target_id = int(input('삭제할 메모 번호: '))
                    target = None
                    for m in memos:
                        if m['id'] == target_id:
                            target = m
                            break

                    if target is None:
                        print('해당 번호의 메모가 없습니다.')
                    else:
                        memos.remove(target)
                        saveMemo()
                        print('메모가 삭제되었습니다.')

                except ValueError:
                    print('숫자를 입력하세요.')

        # ---------- back ----------
        elif choice == config.BACK:
            print('메모 메뉴를 종료합니다.')
            break

        else:
            print('올바른 번호를 입력하세요.')