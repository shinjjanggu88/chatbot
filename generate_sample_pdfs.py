"""
대덕소프트웨어마이스터고등학교 학사정보 샘플 PDF 생성 스크립트
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import os

# 한글 폰트 등록 (Windows 기본 폰트)
try:
    pdfmetrics.registerFont(TTFont('Malgun', 'C:\\Windows\\Fonts\\malgun.ttf'))
except:
    print("경고: 한글 폰트를 찾을 수 없습니다. 기본 폰트로 진행합니다.")

BASE_DIR = Path(__file__).parent
PDF_DIR = BASE_DIR / "pdf"
PDF_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────
# 1. 급식 정보 PDF 생성
# ─────────────────────────────────────────────────────
def create_meal_pdf():
    filename = PDF_DIR / "2_대덕마이스터_급식.pdf"
    doc = SimpleDocTemplate(str(filename), pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=1,  # center
    )

    story = []

    # 제목
    story.append(Paragraph("대덕소프트웨어마이스터고등학교<br/>급식 정보", title_style))
    story.append(Spacer(1, 0.5*cm))

    # 주간 급식표
    story.append(Paragraph("<b>2026년 9월 1주 급식표</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    meal_data = [
        ['요일', '아침', '점심', '저녁'],
        ['월', '계란말이 밥', '돈까스 덮밥', '김밥'],
        ['화', '미역국 밥', '오므라이스', '라면'],
        ['수', '된장국 밥', '제육볶음 밥', '우동'],
        ['목', '콩나물국 밥', '치킨까스', '카레라이스'],
        ['금', '계란탕 밥', '갈비탕', '스파게티'],
        ['토', '휴무', '휴무', '휴무'],
        ['일', '휴무', '휴무', '휴무'],
    ]

    meal_table = Table(meal_data, colWidths=[2*cm, 3*cm, 3*cm, 3*cm])
    meal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))

    story.append(meal_table)
    story.append(Spacer(1, 0.8*cm))

    # 영양정보
    story.append(Paragraph("<b>영양 정보 (9월 1일 기준)</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    nutrition_data = [
        ['구분', '탄수화물', '단백질', '지방', '에너지'],
        ['점심', '73g', '32g', '18g', '650kcal'],
        ['저녁', '68g', '28g', '15g', '580kcal'],
    ]

    nutrition_table = Table(nutrition_data, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    nutrition_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(nutrition_table)
    story.append(Spacer(1, 0.8*cm))

    # 알레르기 정보
    story.append(Paragraph("<b>주요 알레르기 정보</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    allergy_info = """
    <b>알레르기 유발 식품:</b><br/>
    • 계란, 우유, 소고기, 돼지고기, 새우<br/>
    • 견과류 (땅콩, 호두)<br/>
    • 글루텐 함유 식품<br/>
    <br/>
    <i>자세한 정보는 학교 식당 게시판 또는 학교 포털에서 확인하세요.</i>
    """

    story.append(Paragraph(allergy_info, styles['Normal']))

    doc.build(story)
    print(f"✅ 급식 PDF 생성 완료: {filename}")


# ─────────────────────────────────────────────────────
# 2. 시간표 PDF 생성
# ─────────────────────────────────────────────────────
def create_timetable_pdf():
    filename = PDF_DIR / "3_대덕마이스터_시간표.pdf"
    doc = SimpleDocTemplate(str(filename), pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=1,
    )

    story = []

    # 제목
    story.append(Paragraph("대덕소프트웨어마이스터고등학교<br/>학년별 시간표", title_style))
    story.append(Spacer(1, 0.5*cm))

    # 1학년 시간표
    story.append(Paragraph("<b>1학년 시간표 (2026학년도)</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    timetable_data = [
        ['시간', '월', '화', '수', '목', '금'],
        ['08:30~09:20', '국어', '수학', '영어', '과학', '역사'],
        ['09:20~10:10', '국어', '수학', '영어', '과학', '역사'],
        ['10:20~11:10', '프로그래밍', '프로그래밍', '프로그래밍', '프로그래밍', '프로그래밍'],
        ['11:10~12:00', '프로그래밍', '프로그래밍', '프로그래밍', '프로그래밍', '프로그래밍'],
        ['12:00~13:00', '점심시간', '점심시간', '점심시간', '점심시간', '점심시간'],
        ['13:00~13:50', '데이터베이스', '웹개발', '데이터베이스', '웹개발', '회로설계'],
        ['13:50~14:40', '데이터베이스', '웹개발', '데이터베이스', '웹개발', '회로설계'],
        ['14:50~15:40', '체육', '음악', '체육', '미술', '음악'],
        ['15:40~16:30', '체육', '음악', '체육', '미술', '음악'],
    ]

    timetable_table = Table(timetable_data, colWidths=[2*cm, 1.7*cm, 1.7*cm, 1.7*cm, 1.7*cm, 1.7*cm])
    timetable_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0ea5e9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#fef08a')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    story.append(timetable_table)
    story.append(Spacer(1, 0.8*cm))

    # 실습 일정
    story.append(Paragraph("<b>특강/실습 일정</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    special_schedule = """
    <b>2026년 9월</b><br/>
    • 9월 7일(월): AI/머신러닝 특강 (1학년)<br/>
    • 9월 14일(월): 클라우드 컴퓨팅 실습 (2학년)<br/>
    • 9월 21일(월): 사이버보안 특강 (3학년)<br/>
    • 9월 28일(월): 팀 프로젝트 발표 (전학년)<br/>
    <br/>
    <b>학기 중 변동 사항</b><br/>
    학교 공지사항 및 포털을 확인하세요.
    """

    story.append(Paragraph(special_schedule, styles['Normal']))

    doc.build(story)
    print(f"✅ 시간표 PDF 생성 완료: {filename}")


# ─────────────────────────────────────────────────────
# 3. 학사일정 PDF 생성
# ─────────────────────────────────────────────────────
def create_academic_calendar_pdf():
    filename = PDF_DIR / "4_대덕마이스터_학사일정.pdf"
    doc = SimpleDocTemplate(str(filename), pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=1,
    )

    story = []

    # 제목
    story.append(Paragraph("대덕소프트웨어마이스터고등학교<br/>2026학년도 학사일정", title_style))
    story.append(Spacer(1, 0.5*cm))

    # 주요 일정
    story.append(Paragraph("<b>2026학년도 주요 학사일정</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    calendar_data = [
        ['구분', '날짜', '내용', '대상'],
        ['1학기', '2026.03.02', '개학', '전학년'],
        ['', '2026.04.15 ~ 04.17', '1차 지필평가', '전학년'],
        ['', '2026.05.05', '어린이날', '휴무'],
        ['', '2026.05.15', '스포츠데이', '전학년'],
        ['', '2026.06.10 ~ 06.12', '2차 지필평가', '전학년'],
        ['', '2026.07.18', '1학기 종료', '전학년'],
        ['여름방학', '2026.07.19 ~ 08.31', '여름방학', '전학년'],
        ['2학기', '2026.09.01', '개학', '전학년'],
        ['', '2026.10.03 ~ 10.09', '체험학습주간', '2학년'],
        ['', '2026.10.20 ~ 10.22', '3차 지필평가', '전학년'],
        ['', '2026.11.10 ~ 11.12', '4차 지필평가', '전학년'],
        ['', '2026.12.01', '학예발표회', '전학년'],
        ['', '2026.12.18', '2학기 종료', '전학년'],
        ['겨울방학', '2026.12.19 ~ 2027.02.28', '겨울방학', '전학년'],
    ]

    calendar_table = Table(calendar_data, colWidths=[1.5*cm, 2.5*cm, 4*cm, 1.5*cm])
    calendar_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(calendar_table)
    story.append(Spacer(1, 0.8*cm))

    # 주의사항
    story.append(Paragraph("<b>📌 주의사항</b>", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    notices = """
    • 학사일정은 학교 사정에 따라 변경될 수 있습니다.<br/>
    • 정확한 일정은 학교 공식 포털에서 확인하세요.<br/>
    • 각 학년별 추가 일정이 있을 수 있으니 담임 선생님께 확인하세요.<br/>
    • 긴급 공지사항은 학교 앱/문자 알림을 통해 전달됩니다.
    """

    story.append(Paragraph(notices, styles['Normal']))

    doc.build(story)
    print(f"✅ 학사일정 PDF 생성 완료: {filename}")


if __name__ == "__main__":
    print("🚀 대덕소프트웨어마이스터고등학교 샘플 PDF 생성 중...\n")

    try:
        create_meal_pdf()
        create_timetable_pdf()
        create_academic_calendar_pdf()

        print(f"\n✨ 모든 PDF 생성 완료!")
        print(f"📁 저장 위치: {PDF_DIR}")
        print(f"\n다음 단계:")
        print(f"1. 패키지 설치: pip install -r requirements.txt")
        print(f"2. 인덱스 빌드: python rag.py --build")
        print(f"3. 앱 실행: streamlit run main.py")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
