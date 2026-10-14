"""스케줄 실행이 세션 만료로 멈췄을 때 사람에게 알리는 규칙 검증.

실행: py -m pytest scripts/test_naver_expired_alert.py -q

2026-09-17~25(8일)과 10-02~14(12일) 동안 스케줄 실행은 [EXPIRED]를 로그에만 남기고
조용히 멈춰 있었다. 이 PC는 Windows 알림이 꺼져 있어(ToastEnabled=0) 확인 창을 띄운다.
1) 처음 끊긴 실행에서 바로 띄우고, 끊긴 상태가 이어지면 하루 최대 한 번 다시 띄운다.
2) 창을 띄우지 못했으면 기록하지 않아 다음 실행이 다시 시도한다.
3) 서버 검증을 통과한 실행(발행·세션 확인·재로그인)은 기록을 지운다.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import naver_crosspost as nc  # noqa: E402


@pytest.fixture
def prompts(tmp_path, monkeypatch):
    monkeypatch.setattr(nc, "ALERT_FILE", tmp_path / ".expired_alert")
    shown = []
    monkeypatch.setattr(nc, "_show_relogin_prompt", lambda: shown.append(1) or True)
    return shown


# ------------------------------------------------------------ 알림 빈도

def test_first_expired_run_shows_prompt(prompts):
    assert nc.alert_expired(today="2026-10-02") is True
    assert prompts == [1]


def test_same_day_runs_do_not_repeat(prompts):
    nc.alert_expired(today="2026-10-02")
    assert nc.alert_expired(today="2026-10-02") is False
    assert prompts == [1]


def test_reminds_again_next_day_while_still_expired(prompts):
    nc.alert_expired(today="2026-10-02")
    assert nc.alert_expired(today="2026-10-03") is True
    assert prompts == [1, 1]


def test_failed_prompt_is_retried_next_run(tmp_path, monkeypatch):
    monkeypatch.setattr(nc, "ALERT_FILE", tmp_path / ".expired_alert")
    monkeypatch.setattr(nc, "_show_relogin_prompt", lambda: False)
    assert nc.alert_expired(today="2026-10-02") is False
    assert not (tmp_path / ".expired_alert").exists()


def test_relogin_target_exists():
    # 확인 창의 [예]와 바탕화면 아이콘이 이 파일을 연다
    assert nc.RELOGIN_CMD.is_file()


# ------------------------------------------------------------ 확인 창 띄우기

class _Proc:
    def __init__(self, exits_immediately):
        self.exits_immediately = exits_immediately

    def wait(self, timeout=None):
        if self.exits_immediately:
            return 0
        raise subprocess.TimeoutExpired("powershell", timeout)


@pytest.fixture
def popen(monkeypatch):
    """Popen 호출을 기록한다. 첫 시도(작업 객체 탈출)는 거부되는 경우를 흉내 낼 수 있다."""
    calls = []
    state = {"refuse_breakaway": False, "exits_immediately": False}

    def fake(args, creationflags=0, **kw):
        calls.append((args, creationflags))
        if state["refuse_breakaway"] and creationflags & subprocess.CREATE_BREAKAWAY_FROM_JOB:
            raise PermissionError("breakaway not allowed")
        return _Proc(state["exits_immediately"])

    monkeypatch.setattr(subprocess, "Popen", fake)
    return calls, state


@pytest.mark.skipif(sys.platform != "win32", reason="Windows 전용 확인 창")
def test_prompt_is_alive_means_shown(popen):
    calls, _ = popen
    assert nc._show_relogin_prompt() is True
    import base64
    script = base64.b64decode(calls[0][0][-1]).decode("utf-16-le")
    assert str(nc.RELOGIN_CMD) in script and "Popup" in script


@pytest.mark.skipif(sys.platform != "win32", reason="Windows 전용 확인 창")
def test_prompt_that_exits_at_once_is_not_counted_as_shown(popen):
    # DETACHED_PROCESS 때처럼 창 없이 곧바로 끝나면 알린 것으로 치지 않는다(다음 실행이 재시도)
    calls, state = popen
    state["exits_immediately"] = True
    assert nc._show_relogin_prompt() is False


@pytest.mark.skipif(sys.platform != "win32", reason="Windows 전용 확인 창")
def test_prompt_falls_back_when_breakaway_is_refused(popen):
    calls, state = popen
    state["refuse_breakaway"] = True
    assert nc._show_relogin_prompt() is True
    assert [bool(f & subprocess.CREATE_BREAKAWAY_FROM_JOB) for _, f in calls] == [True, False]
    assert all(f & subprocess.CREATE_NO_WINDOW and not f & 0x8 for _, f in calls)  # DETACHED_PROCESS 금지


def test_no_prompt_outside_windows(monkeypatch):
    monkeypatch.setattr(nc.os, "name", "posix")
    assert nc._show_relogin_prompt() is False


# ------------------------------------------------------------ 어느 실행이 알리나

def test_scheduled_expiry_shows_prompt(prompts, monkeypatch):
    monkeypatch.setattr(nc, "is_logged_in", lambda ctx: True)
    monkeypatch.setattr(nc, "verify_login", lambda page: False)
    assert nc.ensure_session(object(), object(), allow_login=False) is False
    assert prompts == [1]


def test_network_failure_is_not_reported_as_expiry(prompts, monkeypatch, capsys):
    # 부팅 직후 와이파이가 붙기 전에 돈 회차가 시간 초과로 '세션 끊김' 창을 띄우면 안 된다
    monkeypatch.setattr(nc, "is_logged_in", lambda ctx: True)
    monkeypatch.setattr(nc, "verify_login", lambda page: None)
    assert nc.ensure_session(object(), object(), allow_login=False) is None
    assert prompts == []
    assert "[EXPIRED]" not in capsys.readouterr().out


def test_unreachable_server_is_inconclusive_not_expired(monkeypatch):
    class Page:
        url = "about:blank"

        def route(self, *a):
            pass

        def unroute(self, *a):
            pass

        def goto(self, *a, **k):
            raise TimeoutError("Page.goto: Timeout 30000ms exceeded")

    assert nc.verify_login(Page()) is None


def test_manual_run_opens_login_window_instead(prompts, monkeypatch):
    monkeypatch.setattr(nc, "is_logged_in", lambda ctx: False)
    monkeypatch.setattr(nc, "do_login", lambda ctx, page, check_existing: False)
    nc.ensure_session(object(), object(), allow_login=True)
    assert prompts == []


# ------------------------------------------------------------ 복구되면 기록을 지운다

class _FakePW:
    def __enter__(self):
        return object()

    def __exit__(self, *exc):
        return False


class _FakeCtx:
    pages = [object()]

    def close(self):
        pass


@pytest.fixture
def run_main(monkeypatch, tmp_path, prompts):
    import playwright.sync_api as pw_api

    monkeypatch.setattr(pw_api, "sync_playwright", lambda: _FakePW())
    monkeypatch.setattr(nc, "launch", lambda pw: _FakeCtx())
    monkeypatch.setattr(nc, "save_cookies", lambda ctx: None)
    monkeypatch.setattr(nc, "collect_pending", lambda *a, **k: [])
    monkeypatch.setattr(nc, "load_json", lambda path, default: default)
    monkeypatch.setattr(nc, "report_session", lambda ctx: None)
    monkeypatch.setattr(nc, "warn_if_expiring", lambda ctx: None)
    monkeypatch.setattr(nc, "RUN_LOCK", tmp_path / ".run.lock")

    def run(*argv, session_ok=True):
        monkeypatch.setattr(nc, "ensure_session", lambda ctx, page, allow_login: session_ok)
        monkeypatch.setattr(nc, "is_logged_in", lambda ctx: session_ok)
        monkeypatch.setattr(nc, "verify_login", lambda page: session_ok)
        monkeypatch.setattr(nc, "do_login", lambda ctx, page, check_existing: session_ok)
        monkeypatch.setattr(sys, "argv", ["naver_crosspost.py", "--no-git-sync", *argv])
        try:
            nc.main()
        except SystemExit as e:
            return e.code
        return None

    return run


def test_verified_publish_run_clears_record(run_main):
    nc.ALERT_FILE.write_text("2026-10-02", encoding="utf-8")
    assert run_main() is None
    assert not nc.ALERT_FILE.exists()


def test_relogin_clears_record(run_main):
    nc.ALERT_FILE.write_text("2026-10-02", encoding="utf-8")
    assert run_main("--login") is None
    assert not nc.ALERT_FILE.exists()


def test_still_expired_run_keeps_record(run_main):
    nc.ALERT_FILE.write_text("2026-10-02", encoding="utf-8")
    assert run_main("--check-session", session_ok=False) == 2
    assert nc.ALERT_FILE.exists()
