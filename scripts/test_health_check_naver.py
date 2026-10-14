"""health_check의 네이버 판정 검증.

실행: py -m pytest scripts/test_health_check_naver.py -q

쿠키에 적힌 만료일은 증거가 아니다. 2026-10-02부터 서버가 세션을 거부했는데도 쿠키는
'만료까지 23일'이라 점검이 정상으로 보였다. 실제 상태는 마지막 스케줄 결과로 본다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import health_check as hc  # noqa: E402


@pytest.mark.parametrize("code, status", [
    ("0", hc.OK),          # 정상 종료
    ("267009", hc.OK),     # 실행 중
    ("2", hc.FAIL),        # [EXPIRED] — 세션이 끊겨 발행이 멈춤
    ("3", hc.OK),          # [BUSY] — 다른 실행과 겹쳐 이번 회차만 건너뜀
    ("1", hc.WARN),        # 그 밖의 실패(예외 등)
])
def test_task_result_judgement(code, status):
    assert hc.judge_naver_task(code)[0] == status


def test_expired_result_says_how_to_recover():
    assert "재로그인" in hc.judge_naver_task("2")[1]


def test_relogin_after_failed_run_is_not_a_failure():
    # 저녁에 재로그인했으면 다음 날 09:30 점검이 전날 16:00 실패를 그대로 '실패'로 보이면 안 된다
    status, note = hc.judge_naver_task("2", relogged_after=True)
    assert status == hc.WARN and "다시 로그인" in note


def test_inconclusive_check_is_a_warning():
    # 4 = 네트워크 등으로 세션을 확인하지 못함. 끊겼다고 단정하지 않는다
    status, note = hc.judge_naver_task("4")
    assert status == hc.WARN and "확인하지 못" in note
