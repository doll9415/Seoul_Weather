import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="서울의 날씨정보", page_icon="🌤")
st.title("🌤 서울의 날씨정보")

# 서울 좌표
lat, lon = 37.5665, 126.9780
st.write(f"📍 위치: 위도 {lat}, 경도 {lon}")

# Open-Meteo 호출 (일별: 최고/최저기온 + 날씨코드)
url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_probability_max"
    "&timezone=Asia%2FSeoul"
)

@st.cache_data(ttl=1800)
def fetch_weather(api_url: str):
    r = requests.get(api_url, timeout=15)
    r.raise_for_status()
    return r.json()

try:
    data = fetch_weather(url)
except Exception as e:
    st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ---- 데이터 파싱
dates = data["daily"]["time"]
tmax = data["daily"]["temperature_2m_max"]
tmin = data["daily"]["temperature_2m_min"]
wcode = data["daily"]["weathercode"]
popmax = data["daily"].get("precipitation_probability_max", [None]*len(dates))

# 요일(KST)
weekdays = [datetime.strptime(d, "%Y-%m-%d").strftime("%a") for d in dates]

# ---- WMO weathercode → 아이콘/설명 매핑
# 참조: https://open-meteo.com/en/docs
WMO_MAP = {
    0: ("☀️", "맑음"),
    1: ("🌤", "대체로 맑음"),
    2: ("⛅️", "구름 조금"),
    3: ("☁️", "흐림"),
    45: ("🌫️", "안개"),
    48: ("🌫️", "착빙성 안개"),
    51: ("🌦️", "가벼운 이슬비"),
    53: ("🌦️", "중간 이슬비"),
    55: ("🌧️", "강한 이슬비"),
    56: ("🌧️", "가벼운 착빙성 이슬비"),
    57: ("🌧️", "강한 착빙성 이슬비"),
    61: ("🌦️", "가벼운 비"),
    63: ("🌧️", "비"),
    65: ("🌧️", "강한 비"),
    66: ("🌧️", "가벼운 어는 비"),
    67: ("🌧️", "강한 어는 비"),
    71: ("🌨️", "가벼운 눈"),
    73: ("🌨️", "눈"),
    75: ("❄️", "강한 눈"),
    77: ("🌨️", "싸락눈"),
    80: ("🌦️", "소나기 (약)"),
    81: ("🌧️", "소나기 (중)"),
    82: ("🌧️", "소나기 (강)"),
    85: ("🌨️", "소나기 눈 (약/중)"),
    86: ("❄️", "소나기 눈 (강)"),
    95: ("⛈️", "뇌우"),
    96: ("⛈️", "뇌우·약한 우박"),
    99: ("⛈️", "뇌우·강한 우박"),
}
icons = [WMO_MAP.get(c, ("❓", "정보 없음"))[0] for c in wcode]
descs = [WMO_MAP.get(c, ("❓", "정보 없음"))[1] for c in wcode]

# ---- 표: 요일별 아이콘/기온
st.subheader("🗓️ 요일별 날씨 요약")
df_table = pd.DataFrame({
    "요일": weekdays,
    "날짜": dates,
    "아이콘": icons,
    "설명": descs,
    "최고기온 (°C)": tmax,
    "최저기온 (°C)": tmin,
    "강수확률 Max (%)": popmax,
})
# 아이콘이 잘 보이도록 column_config 사용
st.dataframe(
    df_table,
    use_container_width=True
)

# ---- 라인차트: 최고/최저 기온 추이
st.subheader("📈 일주일 기온 추이 (최고/최저)")
df_chart = pd.DataFrame({
    "date": pd.to_datetime(dates),
    "최고기온 (°C)": tmax,
    "최저기온 (°C)": tmin,
}).set_index("date")
st.line_chart(df_chart, use_container_width=True)

st.caption("출처: Open-Meteo (무료 공개 API)")
