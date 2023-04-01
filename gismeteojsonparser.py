import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime

datenow = datetime.now()
url = 'https://www.gismeteo.ru/weather-orel-4432/'


def pogoda_today():
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 "
                      "Safari/537.36"})
    soup = bs(response.text, 'html.parser')
    with open('pogoda.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    #Parse Time
    time_widget = soup.find('div', class_='widget-row-time')
    time_span = time_widget.find_all('span')
    time_data=[]
    for time in time_span:
      time_data.append(time.text[:-2] + '-' + time.text[-2:])
    print(time_data)

    #Parse Temperature
    temp_widget = soup.find('div', class_='widget-row-chart-temperature')
    temp_span = temp_widget.find_all('span', class_='unit unit_temperature_c')
    temp_data = []
    for temp in temp_span:
      if temp.text != "°C":
        temp_data.append(temp.text)
    print(temp_data)

    #Parse WindSpeed
    wind_widget = soup.find("div", class_='widget-row-wind-speed')
    wind_span = wind_widget.find_all('span', class_='unit_wind_m_s')
    wind_data = []
    for wind in wind_span:
      if wind.text != "м/c":
        wind_data.append(wind.text)
    print(wind_data)

    #Parse Precipitation
    prec_widget = soup.find('div', attrs = {'data-row': 'precipitation-bars'})
    prec_div = prec_widget.find_all('div', class_='item-unit')
    prec_data = []
    for prec in prec_div:
      prec_data.append(prec.text)
    print(prec_data)

    #Parse Pressure
    press_widget = soup.find('div', class_ = 'widget-row-chart-pressure')#attrs = {'data-row': 'chart'})
    press_span = press_widget.find_all('span', class_='unit_pressure_mm_hg_atm')
    press_data=[]
    for press in press_span:
      if press.text != "мм рт. ст.":
        press_data.append(press.text)
    print(press_data)

    #Parse Humidity
    hum_widget = soup.find('div', class_ = 'widget-row-humidity')#attrs = {'data-row': 'chart'})
    hum_span = hum_widget.find_all('div', class_='row-item')
    hum_data=[]
    for hum in hum_span:
      hum_data.append(hum.text)
    print(hum_data)

    pogoda_data = {'date': str(datenow), 'time':time_data, 'temperature': temp_data, 'windspeed': wind_data, 'precipitation': prec_data, 'pressure': press_data, 'humidity': hum_data}
    print(pogoda_data)
    with open('data_pogoda.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(pogoda_data, ensure_ascii=False, indent=4))


pogoda_today()
