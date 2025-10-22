import streamlit as st
import requests
from datetime import datetime

# 제목
st.title("🌤 서울의 날씨정보")

# 서울의 위도, 경도
lat, lon = 37.5665, 126.9780
st.write(f"📍 위치: 위도 {lat}, 경도 {lon}")

# Open-Meteo API 요청
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FSeoul"
response = requests.get(url)
data = response.json()

# 데이터 파싱
dates = data['daily']['time']
max_temps = data['daily']['temperature_2m_max']
min_temps = data['daily']['temperature_2m_min']

# 요일 이름
weekdays = [datetime.strptime(d, "%Y-%m-%d").strftime("%a") for d in dates]

# 표 만들기
st.subheader("🗓️ 요일별 최고/최저 기온")
weather_table = {
    "요일": weekdays,
    "날짜": dates,
    "최고기온 (°C)": max_temps,
    "최저기온 (°C)": min_temps
}
st.table(weather_table)
