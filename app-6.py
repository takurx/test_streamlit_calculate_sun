import streamlit as st
import datetime
import time
import json
from pysolar.solar import get_altitude, get_azimuth
from astral import LocationInfo
from astral.sun import sun
import pytz

# 設定（任意の場所を設定）
latitude = 35.6895  # 東京の緯度
longitude = 139.6917  # 東京の経度
timezone = "Asia/Tokyo"

st.title("太陽の計算 (今日の日の出時刻、日没時刻、現在時刻の仰角、方位角)")
#st.title("Caluculate about Sun (Sunrise, Sunset, Elevation, Azimuth on Current time)")

st.write('Default latitude = 35.6895, longitude = 139.6917, timezone = "Asia/Tokyo" is 東京')
str_latitude = st.text_input('Please input latitude', value = latitude)
str_longitude = st.text_input('Please input longiture', value = longitude)

latitude = float(str_latitude)
longitude = float(str_longitude)

# 現在時刻表示用プレースホルダー
placeholder = st.empty()
json_placeholder = st.empty()

while True:
    # 現在時刻を取得
    now = datetime.datetime.now(pytz.timezone(timezone))
    
    # 太陽の高度角と方位角を計算
    altitude = get_altitude(latitude, longitude, now)
    azimuth = get_azimuth(latitude, longitude, now)
    
    # 日の出と日没を計算
    location = LocationInfo("Tokyo", "Japan", timezone, latitude, longitude)
    s = sun(location.observer, date=now.date(), tzinfo=pytz.timezone(timezone))
    sunrise = s["sunrise"].strftime("%H:%M:%S")
    sunset = s["sunset"].strftime("%H:%M:%S")
    
    # JSONデータ作成
    solar_data = {
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "altitude": round(altitude, 2),
        "azimuth": round(azimuth, 2),
        "sunrise": sunrise,
        "sunset": sunset
    }
    
    # Streamlitに表示
    placeholder.markdown(f"""
        **現在の時刻:** {solar_data["current_time"]}
        
        **太陽の仰角:** {solar_data["altitude"]}°
        
        **太陽の方位角:** {solar_data["azimuth"]}°
        
        **日の出:** {solar_data["sunrise"]}
        
        **日没:** {solar_data["sunset"]}
    """)
    
    json_placeholder.json(solar_data)
    
    # 1秒待機
    time.sleep(1)

