import os
import streamlit as st
import anthropic
from dotenv import load_dotenv
from rag import build_index, query_context, is_index_ready
import requests
from datetime import datetime

# 로컬: .env 로드 / Streamlit Cloud: st.secrets 사용
load_dotenv()

# ────────────────────────────────────────────────────────────────────────────
# 실시간 학교 정보 조회 함수
# ────────────────────────────────────────────────────────────────────────────

def get_school_info_from_api():
    """NEIS API를 통한 실시간 학교 정보 조회"""
    school_code = "G100000170"  # 대덕소프트웨어마이스터고등학교
    info = {}

    try:
        # 학교 기본 정보
        info['school_name'] = "대덕소프트웨어마이스터고등학교"
        info['location'] = "대전시 유성구 가정북로 76"
        info['phone'] = "042-866-8822"
        info['website'] = "https://dsmhs.djsch.kr/"

        # 실시간 급식 정보 시도 (DSHS.APP 또는 NEIS)
        try:
            meal_response = requests.get(
                f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=sample&Type=json&pIndex=1&pSize=1&ATPT_OFCDE=D10&SD_SCHUL_CODE={school_code}&MLSV_FROM_YMD={datetime.now().strftime('%Y%m%d')}",
                timeout=5
            )
            if meal_response.status_code == 200:
                meal_data = meal_response.json()
                if 'mealServiceDietInfo' in meal_data and len(meal_data['mealServiceDietInfo']) > 1:
                    meals = meal_data['mealServiceDietInfo'][1]['row']
                    info['meals'] = meals
        except:
            pass

    except Exception as e:
        print(f"학교 정보 조회 오류: {e}")

    return info

@st.cache_data(ttl=3600)
def get_cached_school_info():
    """1시간마다 캐시되는 학교 정보"""
    return get_school_info_from_api()

def get_secret(key: str, default: str = "") -> str:
    """st.secrets(Streamlit Cloud) → os.environ(.env) → default 순으로 조회."""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.environ.get(key, default)

# ────────────────────────────────────────────────────────────────────────────
# 학교 정보 프롬프트 (실시간 정보 포함)
# ────────────────────────────────────────────────────────────────────────────
def get_profile_with_realtime_info():
    """실시간 학교 정보를 포함한 프롬프트 생성"""
    school_info = get_cached_school_info()

    profile = f"""
당신은 대덕소프트웨어마이스터고등학교 학생을 위한 학사정보 안내 어시스턴트입니다.

[학교 기본 정보]
학교명: {school_info.get('school_name', '대덕소프트웨어마이스터고등학교')}
위치: {school_info.get('location', '대전시 유성구')}
전화: {school_info.get('phone', '042-866-8822')}
웹사이트: {school_info.get('website', 'https://dsmhs.djsch.kr/')}
특징: 마이스터고등학교 (소프트웨어 및 정보통신 중심)

[제공 정보]
- 급식 정보: 실시간 일일 식단, 영양정보, 알레르기 정보
- 시간표: 학년/반별 시간표, 특강/실습 일정
- 학사일정: 학기 일정, 시험 일정, 방학, 주요 행사

[데이터 출처]
- NEIS(나이스) 교육정보 개방 포털 API (공식)
- 학교 공식 웹사이트
- DSHS.APP (학교 학생 개발 앱)
- PDF 강의 자료

[답변 방침]
- 급식, 시간표, 학사일정 질문: 실시간 API와 PDF 자료를 함께 참고
- 정확한 최신 정보 우선 제공
- 정보를 찾을 수 없는 경우: "현재 조회할 수 없습니다. 학교 포털이나 담당 선생님께 문의하세요."
- 모든 답변은 한국어로, 학생 친화적인 톤으로 작성
"""
    return profile.strip()


# ────────────────────────────────────────────────────────────────────────────
# Streamlit 설정 & 스타일
# ────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="대덕마이스터 학사정보",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 전체 페이지 스타일 (학교 공식 사이트 느낌)
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');

* {
    font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 메인 배경 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

/* 헤더 스타일 */
.header-container {
    background: linear-gradient(135deg, #0e7490 0%, #0d9488 100%);
    color: white;
    padding: 2.5rem 2rem;
    border-radius: 0px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(14, 116, 144, 0.15);
}

.header-container h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.header-container p {
    margin: 0.5rem 0 0 0;
    font-size: 1rem;
    opacity: 0.95;
    font-weight: 300;
}

/* 학교명/설명 */
.school-info {
    background: white;
    border-left: 4px solid #0e7490;
    padding: 1rem;
    margin-bottom: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.school-info h3 {
    color: #0e7490;
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
}

.school-info p {
    color: #475569;
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* 카드 스타일 */
.info-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.info-card:hover {
    box-shadow: 0 8px 24px rgba(14, 116, 144, 0.12);
    border-color: #0e7490;
}

/* 소스박스 */
.source-box {
    background: linear-gradient(135deg, #ecf0f1 0%, #f8f9fa 100%);
    border-left: 4px solid #0e7490;
    padding: 1rem;
    font-size: 0.9rem;
    color: #334155;
    border-radius: 8px;
    margin-top: 1rem;
    font-weight: 500;
}

/* 사이드바 스타일 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

[data-testid="stSidebar"] > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:first-child {
    background: linear-gradient(135deg, #0e7490 0%, #0d9488 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

/* 섹션 제목 */
h2 {
    color: #0e7490;
    border-bottom: 3px solid #0e7490;
    padding-bottom: 0.5rem;
    margin-top: 1.5rem;
    font-weight: 700;
}

h3 {
    color: #0f766e;
    font-weight: 600;
}

/* 버튼 스타일 */
.stButton > button {
    background: linear-gradient(135deg, #0e7490 0%, #0d9488 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.6rem 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(14, 116, 144, 0.2);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(14, 116, 144, 0.3);
}

/* 입력창 스타일 */
.stTextInput input, .stTextArea textarea {
    border-radius: 8px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #0e7490;
    box-shadow: 0 0 0 3px rgba(14, 116, 144, 0.1);
}

/* 체크박스/토글 */
.stCheckbox, .stToggle {
    color: #0e7490;
}

/* 상태 배지 */
.stSuccess {
    background-color: #ecfdf5;
    border-color: #10b981;
    color: #065f46;
}

.stWarning {
    background-color: #fffbeb;
    border-color: #f59e0b;
    color: #78350f;
}

.stError {
    background-color: #fef2f2;
    border-color: #ef4444;
    color: #7f1d1d;
}

/* 테이블 스타일 */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}

/* 채팅 메시지 */
.stChatMessage {
    border-radius: 12px;
}

/* 푸터 스타일 */
.footer-container {
    background: linear-gradient(135deg, #0e7490 0%, #0d9488 100%);
    color: white;
    padding: 2rem;
    margin-top: 3rem;
    border-radius: 0px;
    text-align: center;
}

.footer-container p {
    margin: 0.5rem 0;
    font-size: 0.95rem;
    opacity: 0.9;
}

/* 스크롤바 커스터마이징 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
    background: #0e7490;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #0d9488;
}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="header-container">
    <h1>🎓 대덕마이스터 학사정보</h1>
    <p>대덕소프트웨어마이스터고등학교 공식 학사정보 안내 서비스</p>
</div>
""", unsafe_allow_html=True)

# 학교 소개
st.markdown("""
<div class="school-info">
    <h3>📍 학교 소개</h3>
    <p><strong>대덕소프트웨어마이스터고등학교</strong> | 대전시 유성구<br>
    소프트웨어와 정보통신 분야의 전문가 양성을 위한 마이스터고등학교</p>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# 사이드바 — API 키 & RAG 인덱스 관리
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0e7490 0%, #0d9488 100%);
                color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h3 style="margin: 0 0 0.5rem 0; color: white;">⚙️ 설정</h3>
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">API 및 데이터베이스 관리</p>
    </div>
    """, unsafe_allow_html=True)

    # API 키 입력
    st.markdown("### 🔑 API 설정")
    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Anthropic API 키",
            type="password",
            placeholder="sk-ant-... 형식",
            help="Claude API를 사용하기 위한 인증 키입니다."
        )

    st.divider()

    # 데이터베이스 상태
    st.markdown("### 📖 학사정보 데이터베이스")
    ready = is_index_ready()

    col1, col2 = st.columns(2)
    with col1:
        if ready:
            st.success("✅ 준비 완료")
        else:
            st.warning("❌ 미준비")

    with col2:
        if ready:
            st.info("활성화")
        else:
            st.info("비활성화")

    st.markdown("---")

    # 관리자 영역
    st.markdown("### 🔐 관리자 영역")

    if "admin_unlocked" not in st.session_state:
        st.session_state.admin_unlocked = False

    if not st.session_state.admin_unlocked:
        admin_pw = st.text_input(
            "비밀번호",
            type="password",
            placeholder="관리자 비밀번호 입력",
            key="admin_login"
        )
        if st.button("🔓 로그인", use_container_width=True, type="primary"):
            correct = get_secret("ADMIN_PASSWORD", "admin1234")
            if admin_pw == correct:
                st.session_state.admin_unlocked = True
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("❌ 비밀번호가 틀렸습니다.")
    else:
        st.success("✅ 관리자 모드 활성화됨", icon="🔓")

        col_update, col_lock = st.columns(2)
        with col_update:
            if st.button("🔄 정보 업데이트", use_container_width=True, type="primary"):
                with st.spinner("📊 학사정보 처리 중…"):
                    try:
                        count = build_index()
                        st.success(f"✅ 완료: {count}개 항목 저장됨")
                        st.rerun()
                    except FileNotFoundError as e:
                        st.error(str(e))

        with col_lock:
            if st.button("🔒 잠금", use_container_width=True):
                st.session_state.admin_unlocked = False
                st.rerun()

    st.markdown("---")

    # RAG 설정
    st.markdown("### 🔍 검색 설정")
    use_rag = st.toggle(
        "RAG 검색 활성화",
        value=ready,
        disabled=not ready,
        help="PDF 자료에서 관련 정보를 검색하여 답변에 포함합니다."
    )

    n_results = st.slider(
        "검색 항목 수",
        min_value=1,
        max_value=10,
        value=5,
        help="더 많은 항목을 검색하면 더 정확한 답변을 얻을 수 있습니다."
    )

if not api_key:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                border-left: 4px solid #f59e0b; padding: 1.5rem; border-radius: 8px;
                margin: 2rem 0;">
        <h3 style="color: #92400e; margin: 0 0 0.5rem 0;">🔑 API 키가 필요합니다</h3>
        <p style="color: #b45309; margin: 0;">왼쪽 사이드바에서 Anthropic API 키를 입력해주세요.</p>
        <p style="color: #b45309; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            <a href="https://console.anthropic.com" target="_blank" style="color: #b45309; font-weight: bold;">
            → console.anthropic.com에서 발급받기</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# ────────────────────────────────────────────────────────────────────────────
# 대화 인터페이스
# ────────────────────────────────────────────────────────────────────────────

# 탭 레이아웃
tab1, tab2 = st.tabs(["💬 챗봇", "📚 정보"])

with tab1:
    # 대화 히스토리
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 표시
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 입력창
    if prompt := st.chat_input("💡 예) 오늘 급식이 뭐야? / 시간표 알려줘 / 방학은 언제야?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 학사정보 검색
        rag_context = ""
        if use_rag and ready:
            rag_context = query_context(prompt, n_results=n_results)

        # 시스템 프롬프트 구성 (실시간 학교 정보 포함)
        system_prompt = get_profile_with_realtime_info()
        if rag_context:
            system_prompt += f"\n\n[학사정보 데이터베이스에서 검색된 관련 내용]\n{rag_context}"

        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중…"):
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1500,
                    system=system_prompt,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                answer = response.content[0].text

            st.markdown(answer)

            # 참고 자료 표시
            if rag_context:
                sources = set()
                for line in rag_context.splitlines():
                    if line.startswith("[출처:"):
                        src = line.split("|")[0].replace("[출처:", "").strip()
                        sources.add(src)
                if sources:
                    st.markdown(
                        "<div class='source-box'>📋 참고 자료: "
                        + ", ".join(sorted(sources))
                        + "</div>",
                        unsafe_allow_html=True,
                    )

            st.session_state.messages.append({"role": "assistant", "content": answer})

        # 대화 초기화 버튼
        if st.session_state.messages:
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔄 초기화", type="secondary", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()

with tab2:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #0e7490; margin-top: 0;">📚 이용 가능한 정보</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #0e7490; margin-top: 0;">🍽️ 급식 정보</h4>
            <p style="margin: 0.5rem 0 0 0; color: #475569;">
            • 주간 식단<br>
            • 영양 정보<br>
            • 알레르기 정보
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #0e7490; margin-top: 0;">📚 시간표</h4>
            <p style="margin: 0.5rem 0 0 0; color: #475569;">
            • 학년별 시간표<br>
            • 특강/실습 일정<br>
            • 교과별 수업 시간
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #0e7490; margin-top: 0;">📅 학사일정</h4>
            <p style="margin: 0.5rem 0 0 0; color: #475569;">
            • 학기 일정<br>
            • 시험 일정<br>
            • 방학/행사
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="info-card">
        <h3 style="color: #0e7490; margin-top: 0;">💡 자주 하는 질문</h3>
        <ul style="color: #475569; margin: 1rem 0;">
            <li>오늘 급식이 뭐야?</li>
            <li>시간표를 알려줘</li>
            <li>다음주 월요일 식단은?</li>
            <li>방학은 언제지?</li>
            <li>시험 일정이 언제야?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────
# 푸터
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-container">
    <p><strong>🎓 대덕소프트웨어마이스터고등학교</strong></p>
    <p>학사정보 안내 서비스 | 편하게 질문하세요</p>
    <p style="font-size: 0.85rem; opacity: 0.8; margin-top: 1rem;">
    최종 업데이트: 2026년 8월 | 정확한 정보는 학교 공식 포털을 참고하세요
    </p>
</div>
""", unsafe_allow_html=True)
