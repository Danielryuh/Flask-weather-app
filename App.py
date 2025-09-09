
from flask import Flask, request, render_template, url_for
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather_info = None
    icon_url = None
    temperature = None
    weather_city = None

    if request.method == "POST":
        city = request.form.get("city_name")
        if city:
            api_key = os.getenv("API_KEY")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                weather_main = data['weather'][0]['main'].lower()
                def get_icon_filename(code):
                    if 200 <= code < 300:  # Thunderstorm
                        return "13.thunderstorm-dark.png"
                    elif 300 <= code < 400:  # Drizzle
                        return "20.rain-dark.png"
                    elif 500 <= code < 600:  # Rain
                        return "18.heavy-rain-dark.png"
                    elif 600 <= code < 700:  # Snow
                        return "22.snow-dark.png"
                    elif 700 <= code < 800:  # Atmosphere\
                        return "11.mostly-cloudy-dark.png"
                    elif code == 800:  # Clear
                        return "01.sun-dark.png"
                    elif 801 <= code <= 804:  # Clouds
                        return "05.partial-cloudy-dark.png" if code == 801 else "15.cloud-dark.png" if code == 802 else "11.mostly-cloudy-dark.png"
                    else:
                        return "01.sun-dark.png"

                icon_filename = get_icon_filename(data['weather'][0]['id'])
                icon_url = url_for('static', filename=f'icons/{icon_filename}')

                weather_city = f"{city}"
                weather_info = f"{data['weather'][0]['description']}"
                temperature = round(data['main']['temp'])


            except requests.exceptions.HTTPError:  
                weather_info = "City not found."
            except requests.exceptions.RequestException as e:
                weather_info = f"Request failed: {e}"
        else:
            weather_info = "Please enter a city."

    return render_template("home.html", weather=weather_info, icon=icon_url,
                           temp=temperature, display_city = weather_city
                           )

if __name__ == "__main__":
    app.run(debug=True)