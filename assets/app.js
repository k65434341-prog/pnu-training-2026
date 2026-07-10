/* =====================================================================
   2026 부산대학교 직무연수 안내 — 공용 로직 (index.html / detail.html 공유)
   - 데이터는 하드코딩하지 않고 구글 시트에서 실시간으로 불러옴
   - CSV 파싱은 PapaParse 사용 (쉼표 포함 값 안전 처리)
   ===================================================================== */

/* 시트 연결 설정 — 컬럼명이 바뀌면 여기만 수정하면 됨 */
const CONFIG = {
  // ⚠️ gviz 자동 헤더 감지 오작동 방지를 위해 &headers=1 필수
  SHEET_URL:
    'https://docs.google.com/spreadsheets/d/1HPmYJb-GzbH7OVzxXJw5l6bSA89gK3Wd5aRn3KHrSX0/gviz/tq?tqx=out:csv&headers=1&sheet=data',
};

/* 컬럼 키 (시트 헤더명과 정확히 일치) */
const COL = {
  CODE: '과정코드', NAME: '과정명', FIELD: '분야', TARGET: '대상',
  TYPE: '이수구분', METHOD: '교육방식', HOURS: '교육시간', CAPACITY: '정원',
  PERIOD: '교육기간', APPLY_PERIOD: '신청기간', DEPT: '담당부서',
  SUMMARY: '한줄소개', DESC: '상세소개', GOALS: '학습목표',
  CONTENT: '주요내용', LINK: '신청링크', CONTACT: '문의',
};

/* 강조 필터 팩싯 (순서 = 화면 표시 순서) */
const FACETS = [COL.FIELD, COL.TARGET, COL.TYPE, COL.METHOD, COL.DEPT];

/* 분야별 색상 (배경/글자, 명도대비 AA 고려) */
const FIELD_COLORS = {
  '법정의무교육':    { bg: '#fdeaea', fg: '#b3261e' },
  '대학행정 특화':   { bg: '#e8f0fe', fg: '#1a56b3' },
  '정보화·AI·데이터': { bg: '#e6f6ec', fg: '#1f7a45' },
  '직무공통·문서':   { bg: '#fff2e2', fg: '#a35a09' },
  '예산·회계·계약':   { bg: '#eee9fb', fg: '#5b34b3' },
  '인사·노무':       { bg: '#e4f3f7', fg: '#0e6f8a' },
  '소통·CS·민원':    { bg: '#fce7f0', fg: '#a61e6b' },
  '리더십·역량':     { bg: '#eef2e2', fg: '#5b711b' },
  '안전·보건':       { bg: '#fdece2', fg: '#c2410c' },
  '어학·글로벌':     { bg: '#e7edf9', fg: '#33518a' },
};
const FIELD_COLOR_FALLBACK = { bg: '#eef1f6', fg: '#3a4658' };

function fieldColor(name) {
  return FIELD_COLORS[(name || '').trim()] || FIELD_COLOR_FALLBACK;
}

/* 이수구분 → 배지 종류 */
function typeClass(type) {
  const t = (type || '').trim();
  if (t.startsWith('필수')) return 'badge--required';
  if (t === '권장') return 'badge--recommended';
  return 'badge--optional';
}

/* ---------- 데이터 로더 ---------- */
async function loadCourses() {
  const res = await fetch(CONFIG.SHEET_URL);
  if (!res.ok) throw new Error('시트 응답 오류 (HTTP ' + res.status + ')');
  const text = await res.text();
  const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
  // 과정코드가 있는 행만 (빈 행/합계 행 방어)
  return parsed.data.filter((r) => (r[COL.CODE] || '').trim());
}

/* ---------- 유틸 ---------- */
function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/* " · "(공백+가운뎃점+공백)로만 분리 — 항목 내부 "성희롱·성폭력"은 보존 */
function splitList(s) {
  return String(s || '').split(/\s+·\s+/).map((x) => x.trim()).filter(Boolean);
}

/* URL 쿼리 파라미터 */
function getParam(name) {
  return new URLSearchParams(location.search).get(name);
}

/* 데이터에서 팩싯의 고유 값 추출 (등장 순서 유지) */
function distinctValues(courses, key) {
  const seen = new Set();
  const out = [];
  courses.forEach((c) => {
    const v = (c[key] || '').trim();
    if (v && !seen.has(v)) { seen.add(v); out.push(v); }
  });
  return out;
}
