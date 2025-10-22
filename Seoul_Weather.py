from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def weather():
    # 서울의 위도, 경도
    lat, lon = 37.5665, 126.9780

    # Open-Meteo API URL
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FSeoul"

    # API 요청
    response = requests.get(url)
    data = response.json()

    # 데이터 추출
    dates = data['daily']['time']
    max_temps = data['daily']['temperature_2m_max']
    min_temps = data['daily']['temperature_2m_min']

    # 날짜를 요일 이름으로 변환
    weekdays = [datetime.strptime(d, "%Y-%m-%d").strftime("%a") for d in dates]

    # HTML 템플릿
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>서울의 날씨정보</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background: #f2f2f2; }
            h1 { color: #333; }
            table { margin: auto; border-collapse: collapse; width: 60%; background: white; }
            th, td { border: 1px solid #ccc; padding: 10px; }
            th { background: #007bff; color: white; }
            tr:nth-child(even) { background: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>서울의 날씨정보</h1>
        <h3>위치: 위도 {{ lat }}, 경도 {{ lon }}</h3>
        <table>
            <tr>
                <th>요일</th>
                <th>날짜</th>
                <th>최고기온 (°C)</th>
                <th>최저기온 (°C)</th>
            </tr>
            {% for day, date, tmax, tmin in rows %}
            <tr>
                <td>{{ day }}</td>
                <td>{{ date }}</td>
                <td>{{ tmax }}</td>
                <td>{{ tmin }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    rows = zip(weekdays, dates, max_temps, min_temps)
    return render_template_string(html, lat=lat, lon=lon, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
