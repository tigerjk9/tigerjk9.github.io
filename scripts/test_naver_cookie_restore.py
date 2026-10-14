"""naver_crosspost 쿠키 백업 복원·저장 규칙 검증.

실행: py -m pytest scripts/test_naver_cookie_restore.py -q

백업 파일(cookies.json)이 브라우저 프로필보다 오래된 상태에서 복원되면, 네이버가 이미
갱신해 준 세션 토큰을 옛 토큰으로 덮어쓰게 된다. 아래 두 규칙이 그것을 막는다.
1) 복원은 프로필에 없는 쿠키나 프로필 쪽보다 만료가 늦은(=더 새로 발급된) 쿠키만 넣는다.
2) 세션 검증을 통과한 실행은 어떤 경로로 끝나든 종료 직전에 백업을 갱신한다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import naver_crosspost as nc  # noqa: E402

NOW = 1_800_000_000.0
DAY = 86400.0


def ck(name, value, expires, domain=".naver.com", path="/"):
    return {"name": name, "value": value, "domain": domain, "path": path,
            "expires": expires, "httpOnly": True, "secure": True, "sameSite": "Lax"}


def names(cookies):
    return sorted((c["name"], c["value"]) for c in cookies)


# ------------------------------------------------------------ 복원 규칙

def test_restores_cookies_missing_from_profile():
    backup = [ck("NID_AUT", "a1", NOW + 20 * DAY), ck("NID_SES", "s1", NOW + 25 * DAY)]
    assert names(nc.cookies_to_restore(backup, [], NOW)) == [("NID_AUT", "a1"), ("NID_SES", "s1")]


def test_skips_expired_backup_cookies():
    backup = [ck("NNB", "n1", NOW - 1), ck("NAC", "c1", NOW + DAY)]
    assert names(nc.cookies_to_restore(backup, [], NOW)) == [("NAC", "c1")]


def test_expired_backup_login_restores_no_auth_cookies():
    backup = [ck("NID_AUT", "a1", NOW - 1), ck("NID_SES", "s1", NOW + DAY)]
    assert nc.cookies_to_restore(backup, [], NOW) == []


def test_keeps_session_type_backup_cookies_when_profile_lacks_them():
    backup = [ck("JSESSIONID", "j1", -1, domain="blog.naver.com")]
    assert names(nc.cookies_to_restore(backup, [], NOW)) == [("JSESSIONID", "j1")]


def test_does_not_overwrite_newer_profile_cookie_with_older_backup():
    profile = [ck("NAC", "c2-new", NOW + 29 * DAY)]
    backup = [ck("NAC", "c1-old", NOW + 20 * DAY)]
    assert nc.cookies_to_restore(backup, profile, NOW) == []


def test_overwrites_when_backup_is_newer_than_profile():
    profile = [ck("NAC", "c1-old", NOW + 20 * DAY)]
    backup = [ck("NAC", "c2-new", NOW + 29 * DAY)]
    assert names(nc.cookies_to_restore(backup, profile, NOW)) == [("NAC", "c2-new")]


def test_equal_expiry_keeps_profile_copy():
    profile = [ck("NID_AUT", "profile", NOW + 10 * DAY)]
    backup = [ck("NID_AUT", "backup", NOW + 10 * DAY)]
    assert nc.cookies_to_restore(backup, profile, NOW) == []


def test_same_name_on_other_domain_is_a_different_cookie():
    profile = [ck("NNB", "n-profile", NOW + 300 * DAY, domain=".naver.com")]
    backup = [ck("NNB", "n-blog", NOW + 100 * DAY, domain=".blog.naver.com")]
    assert names(nc.cookies_to_restore(backup, profile, NOW)) == [("NNB", "n-blog")]


# ------------------------------------------------------------ 인증 쌍(NID_AUT·NID_SES·nid_inf)

def test_auth_set_comes_from_backup_when_profile_lost_nid_aut():
    # 프로필에 NID_SES만 남고 NID_AUT가 없으면, 백업의 NID_AUT와 섞지 말고 백업 쌍을 통째로 쓴다
    profile = [ck("NID_SES", "s-profile", NOW + 29 * DAY)]
    backup = [ck("NID_AUT", "a-backup", NOW + 20 * DAY), ck("NID_SES", "s-backup", NOW + 25 * DAY)]
    assert names(nc.cookies_to_restore(backup, profile, NOW)) == [("NID_AUT", "a-backup"), ("NID_SES", "s-backup")]


def test_auth_set_stays_with_profile_for_the_same_login():
    # 같은 로그인(NID_AUT 동일 만료)이면 프로필 쪽 NID_SES가 더 최신이므로 백업은 넣지 않는다
    profile = [ck("NID_AUT", "a", NOW + 20 * DAY), ck("NID_SES", "s-new", NOW + 29 * DAY)]
    backup = [ck("NID_AUT", "a", NOW + 20 * DAY), ck("NID_SES", "s-old", NOW + 22 * DAY)]
    assert nc.cookies_to_restore(backup, profile, NOW) == []


def test_auth_set_from_newer_login_replaces_whole_set():
    # 백업이 더 최근 로그인이면 프로필 NID_SES의 만료가 더 늦어도 백업 쌍 전체를 쓴다
    profile = [ck("NID_AUT", "a-old", NOW + 5 * DAY), ck("NID_SES", "s-old", NOW + 28 * DAY)]
    backup = [ck("NID_AUT", "a-new", NOW + 29 * DAY), ck("NID_SES", "s-new", NOW + 27 * DAY),
              ck("nid_inf", "i-new", NOW + 29 * DAY)]
    assert names(nc.cookies_to_restore(backup, profile, NOW)) == [
        ("NID_AUT", "a-new"), ("NID_SES", "s-new"), ("nid_inf", "i-new")]


# ------------------------------------------------------------ 종료 시 백업 갱신

class _FakePW:
    def __enter__(self):
        return object()

    def __exit__(self, *exc):
        return False


class _FakeCtx:
    def __init__(self):
        self.pages = [object()]
        self.closed = False

    def close(self):
        self.closed = True


@pytest.fixture
def harness(monkeypatch, tmp_path):
    """브라우저 없이 main()의 세션 이후 흐름만 돌린다. 저장 호출을 기록한다."""
    import playwright.sync_api as pw_api

    saved = []
    # 실제 프로필의 실행 잠금을 건드리지 않는다(실행 중인 스케줄 작업과 겹치면 기다리게 된다)
    monkeypatch.setattr(nc, "RUN_LOCK", tmp_path / ".run.lock")
    monkeypatch.setattr(nc, "ALERT_FILE", tmp_path / ".expired_alert")
    monkeypatch.setattr(pw_api, "sync_playwright", lambda: _FakePW())
    monkeypatch.setattr(nc, "launch", lambda pw: _FakeCtx())
    monkeypatch.setattr(nc, "save_cookies", lambda ctx: saved.append(ctx))
    monkeypatch.setattr(nc, "collect_pending", lambda *a, **k: [])
    monkeypatch.setattr(nc, "load_json", lambda path, default: default)
    monkeypatch.setattr(nc, "report_session", lambda ctx: None)
    monkeypatch.setattr(nc, "warn_if_expiring", lambda ctx: None)

    def run(*argv, session_ok=True):
        monkeypatch.setattr(nc, "ensure_session", lambda ctx, page, allow_login: session_ok)
        monkeypatch.setattr(nc, "is_logged_in", lambda ctx: session_ok)
        monkeypatch.setattr(nc, "verify_login", lambda page: session_ok)
        monkeypatch.setattr(sys, "argv", ["naver_crosspost.py", "--no-git-sync", *argv])
        code = None
        try:
            nc.main()
        except SystemExit as e:
            code = e.code
        return list(saved), code

    return run


def test_run_with_nothing_to_publish_still_refreshes_backup(harness):
    # 2026-09-14 23:58 '발행할 포스트가 없습니다' 실행이 백업 없이 끝났고, 다음 실행부터 [EXPIRED]
    saved, code = harness()
    assert (len(saved), code) == (1, None)


def test_check_session_refreshes_backup_when_valid(harness):
    saved, code = harness("--check-session")
    assert (len(saved), code) == (1, 0)


def test_expired_session_never_overwrites_backup(harness):
    assert harness(session_ok=False) == ([], 2)
    assert harness("--check-session", session_ok=False) == ([], 2)
