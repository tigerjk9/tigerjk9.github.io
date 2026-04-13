# Contributing

이 저장소는 개인 블로그 프로젝트입니다. 오타 수정, 버그 제보, 아이디어 제안은 언제든 환영합니다.

## 이슈 제보

- [새 이슈 열기](https://github.com/tigerjk9/tigerjk9.github.io/issues/new)
- 버그의 경우 재현 방법과 환경(OS, Python 버전)을 함께 적어주세요.

## Pull Request

1. 저장소를 fork합니다.
2. `main`에서 브랜치를 만듭니다 (예: `fix/yt-ssl-error`).
3. 변경 후 PR을 열고 내용을 설명합니다.

## 자동화 스크립트 수정 시 주의사항

- `scripts/yt_to_post.py`, `scripts/pdf_to_post.py` 수정 시 `--dry-run`으로 먼저 테스트합니다.
- `.env` 파일은 절대 커밋하지 않습니다. API 키는 `.env.example` 형식만 커밋합니다.
- Python 의존성 추가 시 `scripts/requirements.txt`를 함께 업데이트합니다.
