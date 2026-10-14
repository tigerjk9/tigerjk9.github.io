@echo off
chcp 65001 >nul
rem 네이버 세션이 끊겼을 때 다시 로그인한다. 바탕화면 '네이버 재로그인' 바로가기와
rem 세션 만료 확인 창의 [예]가 이 파일을 연다. 발행은 하지 않는다.
cd /d "%~dp0.."
title 네이버 재로그인
echo 잠시 뒤 뜨는 브라우저 창에서 네이버에 로그인해 주세요. (최대 5분 대기)
echo 창을 직접 닫지 마세요. 로그인이 감지되면 자동으로 닫힙니다.
echo.
py -X utf8 -u scripts\naver_crosspost.py --login --no-git-sync
echo.
echo 서버 기준으로 세션을 다시 확인합니다...
py -X utf8 -u scripts\naver_crosspost.py --check-session --no-git-sync
if %errorlevel%==0 (
  echo.
  echo [완료] 세션이 유효합니다. 다음 스케줄 회차부터 자동 발행이 다시 돕니다.
) else if %errorlevel%==3 (
  echo.
  echo [대기] 다른 크로스포스팅 실행이 아직 브라우저를 쓰고 있습니다. 몇 분 뒤 아이콘을 다시 실행해 주세요.
) else (
  echo.
  echo [확인 필요] 세션이 아직 유효하지 않습니다. 이 창을 닫고 아이콘을 다시 실행해 주세요.
)
echo.
pause
