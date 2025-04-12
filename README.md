# AI 기반 자동 문제 출제 및 채점 시스템

이 프로젝트는 Google Sheets와 연동하여 학생들에게 문제를 제공하고, AI를 활용하여 답안을 채점하고 피드백을 제공하는 시스템입니다.

## 주요 기능

- 학생 정보 입력 및 관리
- Google Sheets에서 문제 가져오기
- 객관식/주관식 문제 지원
- 자동 채점 기능
- AI(OpenAI 또는 Google Gemini)를 활용한 맞춤형 피드백 생성
- 학생 답안 및 결과 저장

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/yourusername/ai-problem-grading-system.git
cd ai-problem-grading-system
```

2. 가상환경 생성 및 활성화
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# MacOS/Linux
python -m venv venv
source venv/bin/activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경변수 설정
`.env` 파일을 생성하고 다음 환경변수를 설정합니다:
```
GOOGLE_SHEETS_API_URL=your_google_sheets_web_app_url
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```

## 실행 방법

```bash
streamlit run app.py
```

## 기술 스택

- Python
- Streamlit
- Google Sheets & Apps Script
- OpenAI API / Google Gemini API

## 프로젝트 구조

```
├── app.py                  # 메인 스트림릿 앱
├── requirements.txt        # 필요한 패키지 목록
├── .env                    # 환경변수 파일 (Git에 포함되지 않음)
├── .gitignore              # Git 무시 파일 목록
└── README.md               # 프로젝트 설명
```

## 라이센스

MIT 라이센스 