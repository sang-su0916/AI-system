import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import openai
import google.generativeai as genai

# .env 파일에서 환경변수 로드
# .env 파일에는 API 키와 같은 민감한 정보를 저장합니다.
load_dotenv()

# 환경변수 설정
GOOGLE_SHEETS_API_URL = os.getenv("GOOGLE_SHEETS_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# API 키 설정
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# 페이지 제목 설정
st.set_page_config(page_title="자동 문제 출제 및 채점 시스템", page_icon="📝", layout="wide")
st.title("자동 문제 출제 및 채점 시스템")

# 세션 상태 초기화
if "current_problem" not in st.session_state:
    st.session_state.current_problem = None
if "student_info" not in st.session_state:
    st.session_state.student_info = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "score" not in st.session_state:
    st.session_state.score = None

# 사이드바 - 학생 정보 입력
with st.sidebar:
    st.header("학생 정보")
    st.markdown("**로그인 방법**")
    st.markdown("1. 학생 ID(학번)를 정확히 입력하세요")
    st.markdown("2. 이름을 실명으로 입력하세요")
    st.markdown("3. 학교 구분과 학년을 선택하세요")
    st.markdown("4. '정보 제출' 버튼을 클릭하세요")
    
    with st.form("student_form"):
        student_id = st.text_input("학생 ID", placeholder="학번을 입력하세요")
        student_name = st.text_input("이름")
        school_type = st.selectbox("학교 구분", options=["중학교", "고등학교"])
        student_grade = st.selectbox("학년", options=["1학년", "2학년", "3학년"])
        subject = st.selectbox("과목", options=["수학", "영어", "국어", "과학", "사회"])
        problem_type = st.selectbox("문제 유형", options=["객관식", "주관식"])
        submit_student_info = st.form_submit_button("정보 제출")
        
        if submit_student_info:
            if student_id and student_name:
                st.session_state.student_info = {
                    "id": student_id,
                    "name": student_name,
                    "school_type": school_type,
                    "grade": student_grade,
                    "subject": subject,
                    "problem_type": problem_type
                }
                st.success(f"{school_type} {student_grade} {student_name} 학생 로그인 성공!")
            else:
                st.error("학생 ID와 이름을 입력해주세요. 학생 ID는 학번을 의미합니다.")

# Google Sheets API에서 문제 가져오기 함수
def get_problem_from_api(subject, problem_type):
    """
    Google Sheets API에서 문제를 가져오는 함수
    """
    try:
        if not GOOGLE_SHEETS_API_URL:
            # 테스트용 가상 데이터 - 기본 20문제 설정
            sample_problems = []
            for i in range(1, 21):  # 20문제 생성
                problem_id = f"P{i:03d}"
                if subject == "수학":
                    if problem_type == "객관식":
                        sample_problem = {
                            "problem_id": problem_id,
                            "subject": subject,
                            "problem_type": problem_type,
                            "content": f"문제 {i}: 다음 중 가장 큰 수는?",
                            "options": ["1.5", "2.3", "0.75", "1.25"],
                            "answer": "2.3",
                            "explanation": "주어진 숫자들 중 2.3이 가장 큽니다.",
                            "keywords": ["비교", "실수", "크기"]
                        }
                    else:
                        sample_problem = {
                            "problem_id": problem_id,
                            "subject": subject,
                            "problem_type": problem_type,
                            "content": f"문제 {i}: 2x + 5 = 15일 때, x의 값은?",
                            "answer": "5",
                            "explanation": "2x + 5 = 15에서 2x = 10이므로 x = 5입니다.",
                            "keywords": ["일차방정식", "계산", "대수"]
                        }
                else:
                    if problem_type == "객관식":
                        sample_problem = {
                            "problem_id": problem_id,
                            "subject": subject,
                            "problem_type": problem_type,
                            "content": f"문제 {i}: 다음 중 올바른 영어 표현은?",
                            "options": ["I am go to school", "I going to school", "I goes to school", "I go to school"],
                            "answer": "I go to school",
                            "explanation": "주어 I와 함께 사용하는 동사의 올바른 형태는 'go'입니다.",
                            "keywords": ["영어", "동사", "문법"]
                        }
                    else:
                        sample_problem = {
                            "problem_id": problem_id,
                            "subject": subject,
                            "problem_type": problem_type,
                            "content": f"문제 {i}: 'apple'의 올바른 철자를 쓰시오.",
                            "answer": "apple",
                            "explanation": "apple은 '사과'를 의미하는 영어 단어입니다.",
                            "keywords": ["영어", "철자", "단어"]
                        }
                sample_problems.append(sample_problem)
            
            # 첫 번째 문제 반환
            return sample_problems[0]
            
        # API 요청 파라미터
        params = {
            "action": "getProblem",
            "subject": subject,
            "problemType": problem_type
        }
        
        # API 호출
        response = requests.get(GOOGLE_SHEETS_API_URL, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 호출 오류: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"문제 가져오기 오류: {str(e)}")
        return None

# 채점 함수
def grade_answer(problem, student_answer):
    """
    학생의 답안을 채점하는 함수
    """
    try:
        correct_answer = problem["answer"]
        
        # 객관식 문제의 경우 정확히 일치하는지 확인
        if problem["problem_type"] == "객관식":
            is_correct = student_answer == correct_answer
            score = 100 if is_correct else 0
        # 주관식 문제의 경우 부분 점수 가능
        else:
            # 여기서는 단순화를 위해 정확히 일치하는 경우만 고려
            is_correct = student_answer.strip().lower() == correct_answer.strip().lower()
            score = 100 if is_correct else 0
            
        return {
            "score": score,
            "is_correct": is_correct
        }
    except Exception as e:
        st.error(f"채점 오류: {str(e)}")
        return {"score": 0, "is_correct": False}

# AI 피드백 생성 함수
def generate_ai_feedback(problem, student_answer, is_correct):
    """
    학생의 답안에 대한 첨삭을 생성하는 함수
    """
    try:
        if OPENAI_API_KEY:
            # OpenAI API를 사용한 첨삭 생성
            prompt = f"""
            문제: {problem['content']}
            정답: {problem['answer']}
            학생 답안: {student_answer}
            정답 여부: {'맞음' if is_correct else '틀림'}
            해설: {problem['explanation']}
            
            위 정보를 바탕으로 학생에게 도움이 될 수 있는 짧은 첨삭을 생성해주세요. 
            틀린 경우, 왜 틀렸는지 설명하고 정답을 이해할 수 있도록 도와주세요.
            맞은 경우, 정답을 더 깊이 이해할 수 있도록 추가 정보를 제공해주세요.
            """
            
            # 최신 버전의 OpenAI API 호출 방식으로 변경
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 학생들의 답안을 첨삭해주는 교육 보조 AI입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            # 응답 처리 방식 변경
            return response.choices[0].message.content.strip()
            
        elif GOOGLE_API_KEY:
            # Google Gemini API를 사용한 첨삭 생성
            prompt = f"""
            문제: {problem['content']}
            정답: {problem['answer']}
            학생 답안: {student_answer}
            정답 여부: {'맞음' if is_correct else '틀림'}
            해설: {problem['explanation']}
            
            위 정보를 바탕으로 학생에게 도움이 될 수 있는 짧은 첨삭을 생성해주세요. 
            틀린 경우, 왜 틀렸는지 설명하고 정답을 이해할 수 있도록 도와주세요.
            맞은 경우, 정답을 더 깊이 이해할 수 있도록 추가 정보를 제공해주세요.
            """
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            return response.text
            
        else:
            # API 키가 없는 경우 기본 첨삭 제공
            if is_correct:
                return f"정답입니다! {problem['explanation']}"
            else:
                return f"틀렸습니다. 정답은 {problem['answer']}입니다. {problem['explanation']}"
    
    except Exception as e:
        st.error(f"첨삭 생성 오류: {str(e)}")
        # 오류 발생 시 기본 첨삭 제공
        if is_correct:
            return f"정답입니다! {problem['explanation']}"
        else:
            return f"틀렸습니다. 정답은 {problem['answer']}입니다. {problem['explanation']}"

# 결과 저장 함수
def save_result_to_api(student_info, problem, student_answer, score, feedback):
    """
    학생의 답안과 결과를 Google Sheets API에 저장하는 함수
    """
    try:
        if not GOOGLE_SHEETS_API_URL:
            # API URL이 없는 경우 저장하지 않음
            return True
            
        # API 요청 데이터
        data = {
            "action": "saveResult",
            "studentId": student_info["id"],
            "studentName": student_info["name"],
            "schoolType": student_info["school_type"],
            "studentGrade": student_info["grade"],
            "problemId": problem["problem_id"],
            "studentAnswer": student_answer,
            "score": score,
            "feedback": feedback
        }
        
        # API 호출
        response = requests.post(GOOGLE_SHEETS_API_URL, json=data)
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"결과 저장 오류: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"결과 저장 오류: {str(e)}")
        return False

# 메인 컨텐츠
if st.session_state.student_info:
    if not st.session_state.current_problem:
        # 문제 가져오기 버튼
        if st.button("문제 가져오기"):
            student_info = st.session_state.student_info
            problem = get_problem_from_api(student_info["subject"], student_info["problem_type"])
            
            if problem:
                st.session_state.current_problem = problem
            else:
                st.error("문제를 가져오는데 실패했습니다.")
    
    if st.session_state.current_problem and not st.session_state.submitted:
        # 문제 표시
        problem = st.session_state.current_problem
        st.header("문제")
        
        # 오류 처리 추가 - 'content' 키가 있는지 확인
        if "content" in problem:
            st.write(problem["content"])
        else:
            st.error("문제 형식이 올바르지 않습니다. 'content' 정보가 없습니다.")
            # 문제를 초기화하고 다시 불러오도록 함
            st.session_state.current_problem = None
            st.button("다시 문제 가져오기")
            st.stop()  # 여기서 처리 중단
        
        # 답안 제출 폼
        with st.form("answer_form"):
            if problem["problem_type"] == "객관식" and "options" in problem:
                student_answer = st.radio(
                    "답안 선택",
                    options=problem["options"],
                    key="student_answer"
                )
            else:
                student_answer = st.text_area("답안 작성", key="student_answer")
            
            submit_answer = st.form_submit_button("답안 제출")
            
            if submit_answer:
                # 채점 - 필요한 키가 있는지 확인
                if "answer" not in problem:
                    st.error("문제 형식이 올바르지 않습니다. '정답' 정보가 없습니다.")
                    st.stop()
                
                grade_result = grade_answer(problem, student_answer)
                score = grade_result["score"]
                is_correct = grade_result["is_correct"]
                
                # 첨삭 생성
                feedback = generate_ai_feedback(problem, student_answer, is_correct)
                
                # 결과 저장
                save_result = save_result_to_api(
                    st.session_state.student_info,
                    problem,
                    student_answer,
                    score,
                    feedback
                )
                
                # 세션 상태 업데이트
                st.session_state.submitted = True
                st.session_state.feedback = feedback
                st.session_state.score = score
                
                st.experimental_rerun()
    
    # 결과 표시
    if st.session_state.submitted:
        st.header("결과")
        problem = st.session_state.current_problem
        
        # 필요한 키가 있는지 확인하는 오류 처리 추가
        if problem is None:
            st.error("문제 정보가 없습니다.")
            st.session_state.submitted = False
            st.button("문제 다시 가져오기")
            st.stop()
        
        # 채점 결과 표시
        st.subheader("📊 채점 결과")
        st.metric("점수", f"{st.session_state.score}점")
        
        # 정답 표시
        st.subheader("✅ 정답")
        if "answer" in problem:
            st.write(problem["answer"])
        else:
            st.write("정답 정보가 없습니다.")
        
        # 해설 표시
        st.subheader("📝 해설")
        if "explanation" in problem:
            st.write(problem["explanation"])
        else:
            st.write("해설 정보가 없습니다.")
        
        # 첨삭 표시
        st.subheader("✍️ 첨삭")
        if st.session_state.feedback:
            st.write(st.session_state.feedback)
        else:
            st.write("첨삭 정보가 없습니다.")
        
        # 새 문제 풀기 버튼
        if st.button("새 문제 풀기"):
            st.session_state.current_problem = None
            st.session_state.submitted = False
            st.session_state.feedback = None
            st.session_state.score = None
            st.experimental_rerun()
else:
    # 학생 정보가 없는 경우 안내 메시지 표시
    st.info("👈 먼저 왼쪽 사이드바에서 학생 정보를 입력해주세요. 학생 ID는 학번을 입력하시면 됩니다.")

# 푸터
st.markdown("---")
st.caption("© 자동 문제 출제 및 채점 시스템") 