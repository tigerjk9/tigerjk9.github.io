"""naver_crosspost 로그인 창이 저절로 꺼지던 문제의 재발 방지 검증.

실행: py -m pytest scripts/test_naver_login_window.py -q

1) 세션 확인(verify_login)은 만료 시 진짜 로그인 폼 대신 안내 화면을 띄운다.
   스케줄 실행·--check-session은 판정 직후 창을 닫으므로, 폼이 보이면 사람이 거기에
   로그인하다가 창이 꺼진다.
2) 브라우저 프로필은 한 번에 한 실행만 쓴다. 두 번째 실행이 브라우저를 띄우면
   TargetClosedError로 죽는다(2026-10-14 재현).
"""
from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import naver_crosspost as nc  # noqa: E402


# ------------------------------------------------------------ 세션 확인 화면

class _FakeRoute:
    def __init__(self):
        self.fulfilled = None

    def fulfill(self, **kw):
        self.fulfilled = kw


class _FakePage:
    """goto 시점에 로그인 폼 요청이 가로채져 있는지 기록한다."""

    def __init__(self, lands_on):
        self.lands_on = lands_on
        self.url = "about:blank"
        self.routes = {}
        self.calls = []

    def route(self, pattern, handler):
        self.calls.append("route")
        self.routes[pattern] = handler

    def unroute(self, pattern, handler=None):
        self.calls.append("unroute")
        self.routes.pop(pattern, None)

    def goto(self, url, **kw):
        self.calls.append("goto")
        # url= 파라미터가 인코딩되지 않은 주소도 가로채야 한다('/'가 섞여 글롭 *에 안 걸린다)
        form = "https://nid.naver.com/nidlogin.login?mode=form&url=https://blog.naver.com/x"
        self.form_hidden_during_goto = any(match(form) for match in self.routes)
        self.url = self.lands_on

    def wait_for_timeout(self, ms):
        pass


def test_probe_hides_login_form_while_checking():
    page = _FakePage("https://nid.naver.com/nidlogin.login?mode=form&url=x")
    assert nc.verify_login(page) is False
    assert page.form_hidden_during_goto
    assert page.calls == ["route", "goto", "unroute"]


def test_probe_releases_interception_even_when_session_is_valid():
    page = _FakePage("https://blog.naver.com/dot_connector/postwrite")
    assert nc.verify_login(page) is True
    assert page.calls == ["route", "goto", "unroute"] and page.routes == {}


def test_probe_notice_tells_the_user_not_to_log_in_there():
    page = _FakePage("https://nid.naver.com/nidlogin.login")
    handler = {}
    page.route = lambda pattern, h: handler.setdefault("h", h)
    nc.verify_login(page)
    route = _FakeRoute()
    handler["h"](route)
    body = route.fulfilled["body"]
    assert route.fulfilled["status"] == 200
    assert "--login" in body and "입력창" in body


# ------------------------------------------------------------ 실행 잠금

@pytest.fixture
def lock_path(tmp_path, monkeypatch):
    monkeypatch.setattr(nc, "PROFILE_DIR", tmp_path)
    monkeypatch.setattr(nc, "RUN_LOCK", tmp_path / ".run.lock")
    monkeypatch.setattr(nc, "LOCK_POLL_SEC", 0.1)
    return tmp_path / ".run.lock"


def test_second_run_is_refused_while_first_holds_profile(lock_path, capsys):
    with nc.run_lock("--limit 10 --no-auto-login", wait_sec=0):
        with pytest.raises(SystemExit) as e:
            with nc.run_lock("--limit 15", wait_sec=0):
                pytest.fail("두 실행이 동시에 프로필을 잡았다")
    assert e.value.code == 3
    out = capsys.readouterr().out
    assert "[BUSY]" in out and "--no-auto-login" in out  # 누가 쥐고 있는지 보여 준다


def test_lock_is_released_when_run_ends(lock_path):
    with nc.run_lock("first", wait_sec=0):
        pass
    with nc.run_lock("second", wait_sec=0):
        pass


def test_lock_is_released_when_run_fails(lock_path):
    with pytest.raises(RuntimeError):
        with nc.run_lock("crashes", wait_sec=0):
            raise RuntimeError("발행 중 예외")
    with nc.run_lock("next", wait_sec=0):
        pass


def test_manual_run_waits_for_short_scheduled_check(lock_path):
    holder = nc.run_lock("--no-auto-login", wait_sec=0)
    holder.__enter__()
    threading.Timer(0.5, holder.__exit__, args=(None, None, None)).start()
    with nc.run_lock("--limit 15", wait_sec=5):  # 기다렸다가 이어서 잡는다
        pass


def test_lock_held_by_another_process_and_freed_when_it_is_killed(lock_path):
    # 실제 상황은 별개 프로세스(스케줄 작업)다. 강제 종료돼도 OS가 잠금을 풀어야 한다
    scripts = Path(nc.__file__).resolve().parent
    code = (f"import sys, time; from pathlib import Path; sys.path.insert(0, r'{scripts}')\n"
            "import naver_crosspost as nc\n"
            f"nc.PROFILE_DIR = Path(r'{lock_path.parent}'); nc.RUN_LOCK = Path(r'{lock_path}')\n"
            "with nc.run_lock('scheduled-holder', 0):\n"
            "    print('LOCKED', flush=True); time.sleep(60)\n")
    proc = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, text=True)
    try:
        assert proc.stdout.readline().strip() == "LOCKED"
        with pytest.raises(SystemExit) as e:
            with nc.run_lock("manual", wait_sec=0):
                pass
        assert e.value.code == 3
    finally:
        proc.kill()
        proc.wait()
    with nc.run_lock("after-kill", wait_sec=2):
        pass


# ------------------------------------------------------------ main() 경로

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
def run_main(monkeypatch, lock_path):
    import playwright.sync_api as pw_api

    launched = []
    ledger_reads = []

    def load_json(path, default):
        if path == nc.STATE_FILE:
            ledger_reads.append(1)
        return default

    monkeypatch.setattr(pw_api, "sync_playwright", lambda: _FakePW())
    monkeypatch.setattr(nc, "launch", lambda pw: launched.append(1) or _FakeCtx())
    monkeypatch.setattr(nc, "save_cookies", lambda ctx: None)
    monkeypatch.setattr(nc, "collect_pending", lambda *a, **k: [])
    monkeypatch.setattr(nc, "load_json", load_json)
    monkeypatch.setattr(nc, "ensure_session", lambda ctx, page, allow_login: True)
    monkeypatch.setattr(nc, "LOCK_WAIT_SEC", 0)
    monkeypatch.setattr(nc, "ALERT_FILE", lock_path.parent / ".expired_alert")

    def runner(*argv):
        monkeypatch.setattr(sys, "argv", ["naver_crosspost.py", "--no-git-sync", *argv])
        launched.clear()
        try:
            nc.main()
        except SystemExit as e:
            return e.code, len(launched)
        return None, len(launched)

    runner.ledger_reads = ledger_reads
    return runner


def test_scheduled_run_skips_without_opening_a_browser_when_busy(run_main):
    with nc.run_lock("--limit 15", wait_sec=0):
        assert run_main("--limit", "10", "--no-auto-login") == (3, 0)


def test_run_proceeds_when_nobody_holds_the_profile(run_main):
    assert run_main("--limit", "10", "--no-auto-login") == (None, 1)


def test_busy_run_does_not_read_the_ledger(run_main):
    # 잠금보다 먼저 읽은 이력은 기다리는 사이 낡는다. 낡은 이력으로 발행·저장하면
    # 방금 끝난 실행의 기록을 덮어쓴다
    with nc.run_lock("--limit 15", wait_sec=0):
        assert run_main("--check-session")[0] == 3
    assert run_main.ledger_reads == []


def test_manual_run_waits_but_scheduled_run_does_not(run_main, monkeypatch):
    monkeypatch.setattr(nc, "LOCK_WAIT_SEC", 5)
    for argv, expected in ((("--limit", "10", "--no-auto-login"), (3, 0)),
                           (("--limit", "15"), (None, 1))):
        holder = nc.run_lock("short-check", wait_sec=0)
        holder.__enter__()
        timer = threading.Timer(0.5, holder.__exit__, args=(None, None, None))
        timer.start()
        try:
            assert run_main(*argv) == expected
        finally:
            timer.join()
