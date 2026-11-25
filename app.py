import streamlit as st
import pandas as pd

# 1. 리스트(list): 바퀴 두께 목록과 강조 수치(위험도 지수) 정의
wheel_thickness_list = [1, 10, 20]
risk_level_list = ["상 (빠짐 위험 높음)", "중 (바퀴 헛돌기 주의)", "하 (안정적 주행 가능)"]

# 2. 함수(def): 지형(terrain)과 바퀴 두께(thickness)를 매개변수로 받아 위험도/결과를 리턴하는 함수
def check_risk(terrain, thickness):
    # 기본 추천 여부와 위험도 계산
    if thickness == 1:
        risk_status = "상"
        advice = "접지면이 너무 좁아 틈새에 끼거나 빠질 위험이 큽니다."
    elif thickness == 10:
        risk_status = "중"
        advice = "일반적인 주행은 가능하나 거친 지형에서는 주의가 필요합니다."
    else:
        risk_status = "하"
        advice = "접지면이 넓어 안정적인 주행이 가능합니다."

    # 3. 조건문(if-elif-else): 진흙 지형이고 바퀴 두께가 20 미만일 때 경고 문구 추가
    if terrain == "진흙" and thickness < 20:
        warning_msg = "⚠️ 진흙 주행 시 주의가 필요합니다! (바퀴 두께 20cm 이상 권장)"
    elif terrain == "사막" and thickness < 10:
        warning_msg = "⚠️ 모래에 바퀴가 빠질 가능성이 높습니다!"
    elif terrain == "물가" or terrain == "늪지":
        warning_msg = "⚠️ 미끄러짐 및 침수 주의 구간입니다!"
    else:
        warning_msg = "✅ 선택한 지형에서 무난하게 주행 가능한 조건입니다."

    return risk_status, advice, warning_msg


# --- Streamlit 웹 화면 구성 시작 ---
st.title("🤖 지형별 로봇 신발(바퀴) 추천 시뮬레이터")
st.write("주행할 지형과 로봇 바퀴 두께를 선택하면 위험도를 분석해 줍니다.")

st.divider()

# 사용자 입력 받기 (기획서 레이아웃 반영)
# (1) 주행 환경 선택 (selectbox)
selected_terrain = st.selectbox(
    "1. 로봇이 주행할 환경을 선택하세요:",
    ["진흙", "사막", "물가", "늪지", "울퉁불퉁한 지형"]
)

# (2) 로봇 바퀴 두께 입력 (슬라이더: 1 ~ 30 cm)
selected_thickness = st.slider(
    "2. 로봇의 바퀴 두께(cm)를 설정하세요:",
    min_value=1,
    max_value=30,
    value=10
)

# 버튼 클릭 시 결과 출력
if st.button("시뮬레이션 결과 확인하기"):
    # 함수 호출하여 결과 받아오기
    risk_result, advice_text, warning_text = check_risk(selected_terrain, selected_thickness)

    st.subheader("📊 분석 결과")

    # 경고 메시지 강조 표시 (st.error / st.warning / st.success 활용)
    if "⚠️" in warning_text:
        st.error(warning_text)
    else:
        st.success(warning_text)

    # 강조 수치(위험도 지수) 표시
    st.metric(label="현재 설정 바퀴의 위험도 등급", value=f"{risk_result} 등급 ({selected_thickness}cm)")
    st.info(f"💡 분석 의견: {advice_text}")

    st.subheader("📋 바퀴 두께별 위험도 비교표")

    # 4. 반복문(for): 바퀴 두께 리스트를 순회하며 테이블 데이터 생성
    table_data = []
    for i in range(len(wheel_thickness_list)):
        current_wheel = wheel_thickness_list[i]
        current_risk = risk_level_list[i]

        # 각 바퀴 두께별로 선택한 지형에서의 추천 여부 판별
        if selected_terrain == "진흙" and current_wheel < 20:
            recommend_note = "비추천 (진흙 빠짐 주의)"
        elif current_wheel == 1:
            recommend_note = "비추천 (접지력 부족)"
        else:
            recommend_note = "추천 가능"

        table_data.append({
            "바퀴 두께 (cm)": f"{current_wheel} cm",
            "기본 위험도": current_risk,
            f"[{selected_terrain}] 지형 적합도": recommend_note
        })

    # 표(테이블) 형태로 화면에 출력
    df = pd.DataFrame(table_data)
    st.table(df)
