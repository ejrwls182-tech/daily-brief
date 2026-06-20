# DailyBrief — 새 노트북 셋업 가이드

매일 아침 7시에 뉴스 대시보드 콘텐츠를 자동 생성·배포하는 시스템을 새 컴퓨터에서 이어서 돌리기 위한 안내서.

## 전체 구조 한눈에

```
Claude 데스크톱 앱 (스케줄 태스크, 매일 7시)
   │  ① WebSearch로 뉴스 검색
   │  ② content.json 생성 (영문 헤드라인+한글제목+단어각주 / 심층분석 영·한 + 출처)
   │  ③ git push
   ▼
GitHub: ejrwls182-tech/daily-brief
   ▼ (auto-deploy)
Vercel: https://daily-brief-virid.vercel.app  ← 라이브 사이트
```

- **3번 탭(식단/일정)** 은 별도 Vercel 앱 임베드: https://new-kakao-talk-bot-2.vercel.app
- 사이트는 순수 정적(index.html + content.json). 서버·빌드 없음.
- **단, 콘텐츠 생성은 Claude 데스크톱 앱이 켜져 있을 때만 실행됨** (앱이 꺼져 있으면 다음 실행 시 돌아감).

---

## 1. 레포 클론

```bash
cd ~
git clone git@github.com:ejrwls182-tech/daily-brief.git news-dashboard
```

SSH가 아직 설정 안 됐으면 아래 2번 먼저.

## 2. GitHub SSH 키 설정 (git push 인증용)

새 노트북에는 SSH 키가 없으므로 새로 만들고 GitHub에 등록해야 함.

```bash
# 키 생성 (이미 ~/.ssh/id_ed25519 있으면 건너뜀)
ssh-keygen -t ed25519 -C "ejrwls182@gmail.com" -f ~/.ssh/id_ed25519 -N ""

# 공개키 출력 → 복사
cat ~/.ssh/id_ed25519.pub
```

출력된 키를 https://github.com/settings/ssh/new 에 등록 (Title 아무거나).

연결 확인:
```bash
ssh -T git@github.com   # "Hi ejrwls182-tech!" 나오면 성공
```

remote가 https로 돼 있으면 ssh로 변경:
```bash
cd ~/news-dashboard
git remote set-url origin git@github.com:ejrwls182-tech/daily-brief.git
```

## 3. Claude 스케줄 태스크 재생성

새 노트북의 Claude 데스크톱 앱에서, Claude에게 아래를 그대로 요청하면 됨:

> "매일 오전 7시에 실행되는 스케줄 태스크를 만들어줘. taskId는 daily-dashboard-content. 프롬프트는 ~/news-dashboard/TASK_PROMPT.md 파일 내용을 그대로 써줘."

또는 직접 만들 때 cron은 `0 7 * * *`, 프롬프트는 [TASK_PROMPT.md](TASK_PROMPT.md) 참고.

생성 후 사이드바 Scheduled → `daily-dashboard-content` → **Run now** 한 번 눌러서 WebSearch·git push 권한을 미리 승인해두면 이후 자동 실행됨.

## 4. 동작 확인

```bash
# 로컬에서 미리보기 (선택)
python3 -m http.server 8765 --directory ~/news-dashboard
# → http://localhost:8765
```

라이브 확인: https://daily-brief-virid.vercel.app

---

## 핵심 정보 요약

| 항목 | 값 |
|---|---|
| GitHub 레포 | `git@github.com:ejrwls182-tech/daily-brief.git` |
| 로컬 경로 | `~/news-dashboard` |
| 라이브 URL | https://daily-brief-virid.vercel.app |
| 3번 탭 임베드 | https://new-kakao-talk-bot-2.vercel.app |
| 스케줄 | 매일 07:00 (cron `0 7 * * *`) |
| taskId | `daily-dashboard-content` |
| 배포 | GitHub push → Vercel 자동 |

## 파일 구성

- `index.html` — 대시보드 UI (3탭: News / Analysis / Schedule)
- `content.json` — 매일 갱신되는 콘텐츠 (스케줄 태스크가 덮어씀)
- `vercel.json` — Vercel 설정 (content.json 캐시 비활성화)
- `TASK_PROMPT.md` — 스케줄 태스크 프롬프트 원문
- `SETUP.md` — 이 문서

## 참고

- 컴퓨터가 꺼져 있어도 자동화하려면 Anthropic API + Vercel Cron 방식이 필요(유료, 월 ~$5~15). 현재는 Claude 앱 스케줄(무료, 앱 켜져 있을 때) 방식.
