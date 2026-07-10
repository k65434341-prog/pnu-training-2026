# 2026 부산대학교 직무연수 안내

부산대학교 교직원을 위한 2026년 직무연수 과정을 안내하는 정적 웹사이트입니다.
데이터는 구글 시트에서 **페이지 로드 시 실시간으로** 불러오며, 시트를 수정하면 새로고침만으로 사이트에 반영됩니다.

## 구성

| 파일 | 설명 |
|------|------|
| `index.html` | 메인 — 과정 목록, 통합 검색, 분야·대상·이수구분·교육방식·담당부서 필터 |
| `detail.html` | 상세 — `?code=과정코드`로 특정 과정의 전체 정보 표시 |
| `assets/styles.css` | 공용 디자인 시스템 |
| `assets/app.js` | 공용 로직 — 구글 시트 로드(PapaParse), 렌더 헬퍼 |

> `index.html`, `detail.html`, `assets/` 3가지가 배포에 필요한 전부입니다.
> (그 외 `작업기획서.md`, `*.py`, `sheet_data.csv` 등은 기획·검증용 자료입니다.)

## 데이터 소스

- 구글 시트(공개: 링크가 있는 모든 사용자·뷰어)에서 gviz CSV로 로드합니다.
- **주의**: `&headers=1`을 반드시 포함해야 헤더가 1행으로 인식되어 32개 과정이 정상 분리됩니다.
  ```
  https://docs.google.com/spreadsheets/d/1HPmYJb-GzbH7OVzxXJw5l6bSA89gK3Wd5aRn3KHrSX0/gviz/tq?tqx=out:csv&headers=1&sheet=data
  ```
- 쉼표 포함 값 안전 처리를 위해 PapaParse로 파싱합니다.
- 시트 URL·컬럼명은 `assets/app.js` 상단(`CONFIG`, `COL`)에서 한 곳에서 관리합니다.

## 로컬 실행

```bash
# 폴더에서 로컬 서버 실행 (file:// 로 직접 열면 fetch가 막힙니다)
python -m http.server 8899
# 브라우저에서 http://localhost:8899/ 접속
```

## GitHub Pages 배포

1. GitHub에서 **Public** 저장소 생성 (예: `pnu-training-2026`).
2. `index.html`, `detail.html`, `assets/` 업로드 (웹 UI 드래그 또는 git push).
3. **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`** 저장.
4. 발급되는 `https://{사용자}.github.io/{저장소}/` 로 접속 확인.

## 유지보수

- 과정 추가/수정: 구글 시트만 편집하면 됩니다(코드 수정 불필요). 필터 옵션도 시트 값에서 자동 생성됩니다.
- 컬럼명 변경 시: `assets/app.js`의 `COL` 상수만 맞춰 수정하세요.
