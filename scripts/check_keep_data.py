"""
Google Keep 데이터 형식 확인 스크립트

Google Keep에서 "투자" 라벨의 메모를 가져와서 데이터 형식을 분석합니다.
"""

import gkeepapi


def fetch_investment_notes(email: str, password: str, label: str = "투자"):
    """
    Google Keep에서 지정된 라벨의 메모를 가져옵니다.

    Args:
        email: Google 계정 이메일
        password: Google 계정 비밀번호 (또는 앱 비밀번호)
        label: 찾을 라벨 이름

    Returns:
        라벨에 해당하는 메모 리스트
    """
    # Google Keep 로그인
    keep = gkeepapi.login(email, password)

    # 라벨 찾기
    labels = keep.findLabels([label])
    if not labels:
        print(f"라벨 '{label}'을 찾을 수 없습니다.")
        return []

    label_id = labels[0].id

    # 해당 라벨의 메모 찾기
    notes = []
    for note in keep.all():
        if label_id in note.labels.all():
            notes.append(note)

    return notes


def analyze_note_format(notes: list):
    """
    메모의 형식을 분석합니다.

    Args:
        notes: Google Keep 노트 리스트
    """
    if not notes:
        print("투자 관련 메모가 없습니다.")
        return

    print(f"\n{'='*60}")
    print(f"총 {len(notes)}개의 투자 메모를 찾았습니다.")
    print(f"{'='*60}\n")

    for idx, note in enumerate(notes, 1):
        print(f"[메모 {idx}] {note.title}")
        print(f"{'-'*60}")
        print(f"내용:\n{note.text}")
        print(f"\n체크리스트 항목: {len(note.items)}개")
        for i, item in enumerate(note.items, 1):
            checked = "☑" if item.checked else "☐"
            print(f"  {checked} {item.text}")
        print()


if __name__ == "__main__":
    # Google Keep 인증 정보 입력
    print("Google Keep 인증 정보를 입력하세요.")
    email = input("이메일: ")
    password = input("비밀번호 (또는 앱 비밀번호): ")

    # 투자 메모 가져오기
    notes = fetch_investment_notes(email, password, "투자")

    # 형식 분석
    analyze_note_format(notes)
