import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_Label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temp_Label = QLabel(self)
        self.emoji_Label = QLabel(self)
        self.description_Label = QLabel(self)
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_Label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_Label)
        vbox.addWidget(self.emoji_Label)
        vbox.addWidget(self.description_Label)
        
        self.setLayout(vbox)
        
        self.city_Label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_Label.setAlignment(Qt.AlignCenter)
        self.emoji_Label.setAlignment(Qt.AlignCenter)
        self.description_Label.setAlignment(Qt.AlignCenter)
        
        self.city_Label.setObjectName("city_Label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_Label.setObjectName("temp_Label")
        self.emoji_Label.setObjectName("emoji_Label")
        self.description_Label.setObjectName("description_Label")
        
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            Qlabel#city_Label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temp_Label{
                font-size: 75px;
            }
            QLabel#emoji_Label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_Label{
                font-size: 50px;
            }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
        
    def get_weather(self):
        api_key = "ad63426974f86bfb69405c624ffa3783"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            
            match response.status_code:
                
                case 400:
                    self.display_error("Bad Request")
                case 401:
                    self.display_error("Unauthorized")
                case 403:
                    self.display_error("Forbidden")
                case 404:
                    self.display_error("Not Found")
                case 500:
                    self.display_error("Internal Server Error")
                case 502:
                    self.display_error("Bad Gateway")
                case 503:
                    self.display_error("Service Unavailable")
                case 504:
                    self.display_error("Gateway Timeout")
                case _:
                    self.display_error(f"HTTP Error {http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects")
                
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error: {req_error}")
        
    def display_error(self, message):
        self.temp_Label.setStyleSheet("font-size: 30px;")
        self.temp_Label.setText(message)
        self.emoji_Label.clear()
        self.description_Label.clear()
    
    def display_weather(self, data):
        self.temp_Label.setStyleSheet("font-size: 75px;")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_desc = data["weather"][0]["description"]
        
        self.temp_Label.setText(f"{temp_c:.0f}°C")
        self.emoji_Label.setText(self.get_weather_emoji(weather_id))
        self.description_Label.setText(weather_desc)
        
    def get_weather_emoji(self, weather_id):
        
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())