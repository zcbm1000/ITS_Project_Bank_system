# ==========================================================
# dm_memo_must/memo/memo_final.py
# 역할: 메모 관리 메뉴 전체 (저장/불러오기 + 입출력 + 흐름)
# ==========================================================

import json
from config import config
from dataBase import memoDb
from datetime import datetime

# [수정 전]
# import os  ← os 모듈 사용
#
# [수정 후]
# os import 제거. loadMemo 에서 try/except 로 대체.
#
# [왜 이렇게 해야 하는가]
# os.path.exists() 는 파일 존재 여부 확인용인데
# try/except FileNotFoundError 로 완전히 대체 가능함.
# 배우지 않은 모듈을 쓸 필요가 없고, 코드도 더 간결해짐.

MEMO_DB_PATH = 'memo_db.json'


def get_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def saveMemo():
    # memoDb.memos 를 memo_db.json 에 저장.
    with open(MEMO_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(memoDb.memos, f, ensure_ascii=False, indent=2)


def loadMemo():
    # [수정 전]
    # if os.path.exists(MEMO_DB_PATH):
    #     with open(...) as f:
    #         memoDb.memos = json.load(f)
    #
    # [수정 후]
    # try/except FileNotFoundError 로 대체.
    # 파일이 없으면 FileNotFoundError 가 발생하는데 pass 로 넘김.
    # 파일이 없다 = 처음 실행이다 = 빈 딕셔너리 그대로 쓰면 됨.
    try:
        with open(MEMO_DB_PATH, 'r', encoding='utf-8') as f:
            memoDb.memos = json.load(f)
    except FileNotFoundError:
        pass


def initUser(userId):
    # 해당 유저의 메모 리스트가 없으면 빈 리스트로 초기화.
    if userId not in memoDb.memos:
        memoDb.memos[userId] = []


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
            if len(memos) >= config.MAX_MEMO_COUNT:
                print(f'메모는 최대 {config.MAX_MEMO_COUNT}개까지 작성할 수 있습니다.')
            else:
                while True:
                    title = input(f'제목을 입력하세요 ({config.MAX_MEMO_TITLE_LENGTH}자 이하): ')
                    if len(title) == 0:
                        print('제목을 입력해주세요.')
                    elif len(title) > config.MAX_MEMO_TITLE_LENGTH:
                        print(f'{config.MAX_MEMO_TITLE_LENGTH}자를 초과했습니다. ({len(title)}자)')
                    else:
                        break

                while True:
                    content = input(f'내용을 입력하세요 ({config.MAX_MEMO_LENGTH}자 이하): ')
                    if len(content) == 0:
                        print('내용을 입력해주세요.')
                    elif len(content) > config.MAX_MEMO_LENGTH:
                        print(f'{config.MAX_MEMO_LENGTH}자를 초과했습니다. ({len(content)}자)')
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
                        while True:
                            new_title = input(f'새 제목 ({config.MAX_MEMO_TITLE_LENGTH}자 이하, 엔터 시 유지): ')
                            if new_title == '':
                                new_title = target['title']
                                break
                            elif len(new_title) > config.MAX_MEMO_TITLE_LENGTH:
                                print(f'{config.MAX_MEMO_TITLE_LENGTH}자를 초과했습니다.')
                            else:
                                break

                        while True:
                            new_content = input(f'새 내용 ({config.MAX_MEMO_LENGTH}자 이하, 엔터 시 유지): ')
                            if new_content == '':
                                new_content = target['content']
                                break
                            elif len(new_content) > config.MAX_MEMO_LENGTH:
                                print(f'{config.MAX_MEMO_LENGTH}자를 초과했습니다.')
                            else:
                                break

                        target['title']        = new_title
                        target['content']      = new_content
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
