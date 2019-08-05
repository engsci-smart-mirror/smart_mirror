import time
import tkinter
import requests

from datetime import datetime
from tkinter.ttk import *


class SmartMirrorGui(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self._frame = None
        self.switch_frame(SignInPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class SignInPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="Welcome to your Smart mirror. Please hold still while we sign you in.")\
            .pack(side="top", pady=10)
        self.label = tkinter.Label(self)
        self.label.pack(side="top", pady=30)
        self.counter(2, master)

    def counter(self, number, master):
        self.label['text'] = number
        if number > 0:
            self.after(1000, self.counter, number-1, master)
        else:
            master.switch_frame(SetupPage)


class SetupPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="Recognized Face.").pack(side="top", pady=10)
        name = 'Kelly'
        tkinter.Label(self, text="Hi " + name).pack(side="top", pady=10)
        tkinter.Label(self, text="Please wait while we set things up for you").pack(side="top", pady=10)
        self.progress = Progressbar(self, orient='horizontal', length=100, mode='determinate')
        self.progress.pack(pady=10)
        self.progressbar(0, master)

    def progressbar(self, number, master):
        self.progress['value'] = number
        if number != 100:
            self.after(10, self.progressbar, number+1, master)
        else:
            master.switch_frame(MainPage)


class MainPage(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        tkinter.Label(self, text="Time").pack(side="top", pady=10)
        self.timer = tkinter.Label(self)
        self.timer.pack(side="top", pady=10)
        self.weather = tkinter.Label(self)
        self.weather.pack(side='top', pady=10)
        self.ticking_time()
        self.get_weather()

    def ticking_time(self):
        time_string = time.strftime("%H:%M:%S")
        self.timer['text'] = time_string
        self.timer.after(200, self.ticking_time)

    def get_weather(self):
        # Toronto City id
        city_id = '6167865'
        weather_key = 'ab1a9d34244c62a5053bf8755075d615'
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': weather_key, 'id': city_id, 'units': 'metric'}
        response = requests.get(url, params)
        weather = response.json()
        weather_dict = self.parse_weather(weather)
        self.weather['text'] = str(weather_dict)

    @staticmethod
    def parse_weather(weather):
        weather_dictionary = {
            'condition': weather['weather'][0]['description'],
            'temperature': weather['main']['temp'],
            'min_temp': weather['main']['temp_min'],
            'max_temp': weather['main']['temp_max'],
            'humidity': weather['main']['humidity'],
            'pressure': weather['main']['pressure'],
            'wind_speed': weather['wind']['speed'],
            'sunrise': datetime.fromtimestamp(weather['sys']['sunrise']).strftime("%m/%d/%Y, %H:%M:%S"),
            'sunset': datetime.fromtimestamp(weather['sys']['sunset']).strftime("%m/%d/%Y, %H:%M:%S"),
            'time': datetime.fromtimestamp(weather['dt']).strftime("%m/%d/%Y, %H:%M:%S"),
            'location': weather['name']
        }
        return weather_dictionary


if __name__ == "__main__":
    GUI = SmartMirrorGui()
    GUI.mainloop()
