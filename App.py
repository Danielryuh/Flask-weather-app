
from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather_info = None
    icon_url = None
    temperature = None

    if request.method == "POST":
        city = request.form.get("city_name")
        if city:
            api_key = os.getenv("API_KEY")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

            try:
                response = requests.get(url)
                response.raise_for_status()  # raises HTTPError if not 200
                data = response.json()
                weather_info = f"Weather in {city}: {data['weather'][0]['description']}"
                temperature = round(data['main']['temp'])  # in Celsius
                icon_code = data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            except requests.exceptions.HTTPError:
                weather_info = "City not found."
            except requests.exceptions.RequestException as e:
                weather_info = f"Request failed: {e}"
        else:
            weather_info = "Please enter a city."

    return render_template("home.html", weather=weather_info, icon=icon_url, temp=temperature)

if __name__ == "__main__":
    app.run(debug=True)