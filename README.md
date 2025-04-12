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
git clone https://github.com/sang-su0916/AI-system.git
cd AI-system
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

## 배포 방법

### Streamlit Cloud 배포

1. GitHub에 코드를 푸시합니다.
2. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인합니다.
3. "New app" 버튼을 클릭합니다.
4. GitHub 저장소, 브랜치, 메인 파일(app.py)을 선택합니다.
5. "Advanced Settings"에서 Python 버전을 3.11로 설정합니다.
6. "Secrets" 섹션에서 다음 내용을 추가합니다:
   ```
   GOOGLE_SHEETS_API_URL = "your_google_sheets_web_app_url"
   OPENAI_API_KEY = "your_openai_api_key"
   GOOGLE_API_KEY = "your_google_api_key"
   ```
7. "Deploy" 버튼을 클릭하여 배포합니다.

### Heroku 배포

1. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)를 설치합니다.
2. Heroku에 로그인합니다:
   ```bash
   heroku login
   ```
3. Heroku 앱을 생성합니다:
   ```bash
   heroku create your-app-name
   ```
4. 환경변수를 설정합니다:
   ```bash
   heroku config:set GOOGLE_SHEETS_API_URL=your_google_sheets_web_app_url
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set GOOGLE_API_KEY=your_google_api_key
   ```
5. 코드를 푸시하여 배포합니다:
   ```bash
   git push heroku main
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
├── .streamlit/             # Streamlit 설정 파일
│   ├── config.toml         # 일반 설정
│   └── secrets.toml        # 시크릿 설정 (Git에 포함되지 않음)
├── Procfile                # Heroku 배포 설정
├── setup.sh                # 서버 설정 스크립트
├── runtime.txt             # Python 버전 지정
├── .gitignore              # Git 무시 파일 목록
└── README.md               # 프로젝트 설명
```

## 라이센스

MIT 라이센스 