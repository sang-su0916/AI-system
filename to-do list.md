# 📝 AI 기반 자동 문제 출제 및 채점 시스템 개발 To-Do List

## 1️⃣ Google Sheets & Apps Script 설정 (Day 1-2)

### Google Sheets 구조 설정
- [x] `problems` 시트 생성 및 컬럼 구조 설정
  - 문제ID, 과목, 문제유형, 문제내용, 보기1~5, 정답, 해설, 키워드
- [x] `student_answers` 시트 생성 및 컬럼 구조 설정
  - 학생ID, 이름, 학년, 문제ID, 제출답안, 점수, 피드백, 제출시간
- [x] `student_weaknesses` 시트 생성 및 컬럼 구조 설정
  - 학생ID, 이름, 약점 키워드, 오답률
- [x] 샘플 데이터 입력 및 테스트

### Apps Script API 개발 (Day 3-4)
- [x] 프로젝트 생성 및 기본 설정
- [x] 문제 제공 API 개발
  - [x] 랜덤 문제 선택 로직
  - [x] 조건별 문제 필터링 기능
- [x] 채점 API 개발
  - [x] 답안 비교 로직
  - [x] 점수 계산 기능
- [x] 결과 저장 API 개발
  - [x] student_answers 시트에 기록
  - [x] student_weaknesses 시트 업데이트
- [x] API 배포 및 웹앱 URL 생성

## 2️⃣ Streamlit 앱 개발 (Day 5-6)

### 환경 설정
- [x] Python 가상환경 생성
- [x] 필요한 패키지 설치 및 requirements.txt 생성
  - streamlit
  - google-api-python-client
  - python-dotenv
  - openai/google-generativeai

### 프론트엔드 개발
- [x] 기본 UI 구조 설계
- [x] 학생 정보 입력 폼 구현
- [x] 문제 표시 화면 구현
- [x] 답안 제출 폼 구현
- [x] 결과 및 피드백 표시 화면 구현

### API 연동
- [x] Google Apps Script API 연동
- [x] 환경변수 설정 (.env)
- [x] API 호출 함수 구현

## 3️⃣ AI 피드백 시스템 구현 (Day 7)

### OpenAI/Gemini API 연동
- [x] API 키 설정
- [x] 프롬프트 템플릿 작성
- [x] 피드백 생성 함수 구현
- [x] 에러 처리 및 백업 로직 구현

## 4️⃣ 테스트 및 최적화 (Day 8)

### 테스트
- [x] 단위 테스트 작성 및 실행
- [x] 통합 테스트 수행
- [x] 사용자 시나리오 테스트
- [x] 버그 수정 및 개선

### 약점 분석 시스템
- [x] 오답률 계산 로직 구현
- [x] 약점 키워드 추출 기능
- [x] 맞춤형 문제 추천 알고리즘 구현

## 5️⃣ 배포 및 문서화

### 배포
- [x] Streamlit Cloud 배포
- [x] 환경변수 설정
- [x] 보안 설정 확인

### 문서화
- [x] API 문서 작성
- [x] 사용자 매뉴얼 작성
- [x] 시스템 아키텍처 문서 작성
- [x] 유지보수 가이드 작성

## 🔄 추후 확장 기능 (Optional)
- [x] 이메일/카톡 자동 알림 기능
- [x] 학생별 맞춤 학습 플랜 생성
- [x] 학부모용 주간 리포트 PDF 자동 발송 