import tkinter as tk
from tkinter.simpledialog import askstring
from fnc import btn_pressed


class MainWindow(tk.Tk):
    def __init__(self, threadworker):
        super().__init__()
        self.title('WeatherTk')
        #self.geometry('410x330')

        self.lab1 = tk.Label(self)
        self.lab1.configure(text="Enter city:")
        self.lab1.pack()

        self.input = InputFrame(self)
        self.input.pack()

        self.status_label = tk.Label(self)
        self.status_label.pack()

        self.current_weather_frame = CurrentWeatherFrame(self)
        self.space_label = tk.Label(self, text = " ")
        # this label is used to create e bit of space between the two frames
        self.forecast_daily_frame = ForecastDailyFrame(self)
        # these two frames and the label get packed after weather is fetched

        # the following dict is used to cache icons in memory
        # this is only a "temporary" solution and will be changed "soon"
        self.icon_cache = dict()

        self.threadworker = threadworker

        self.WEATHER_CURRENT_URL = "http://api.openweathermap.org/data/2.5/weather?"
        self.WEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/onecall?"
        self.UNIT = "metric"    # TODO: add option in the gui to change the unit
        self.API_KEY = self.init_api_key()

    def init_api_key(self):
        # reads openweathermap api key
        # from a file named api_key.txt in the same directory where the main script of the app is run from
        # it must be a plain text file, only containing the api key
        # TODO: just realized that I should not be openning a file from tkinter's main thread, will fix it "soon"

        # if the file is not found then the user is prompted to enter an api key
        # TODO: save the user entered api key to api_key.txt after a successful paste
        # TODO: probably add test to determine if it's a "correct" api key

        try:
            with open("api_key.txt") as keyfile:
                api_key = keyfile.read().rstrip("\n")    # striping it in case there's an empty line at the end of the file
        except:
            self.status_label.configure(text = "error openning api_key.txt")    # asking the user to enter the key in the next line
            api_key = askstring(title = "api_key.txt not found", prompt = "Please enter api key: ", parent = self)
            if api_key is None or api_key == "":
                # if api_key.txt not found and user enters no key:
                self.input.get_btn.configure(state=tk.DISABLED)
                self.status_label.configure(text = "No API key provided")
            else:
                # if the user enters the key:
                self.status_label.configure(text = "")
        return api_key


class InputFrame(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.inp_text = tk.StringVar()
        self.inp_text.set("London")

        self.inp = tk.Entry(self, textvariable=self.inp_text)
        self.inp.grid(row=0,column=1)
        self.inp.bind('<Return>', lambda x: parent.threadworker.submit(btn_pressed, parent, self.inp.get()))

        #self.get_btn = tk.Button(self, text="Submit", command=lambda: btn_pressed(parent, self.inp.get()))
        self.get_btn = tk.Button(self, text="Submit", command=lambda: parent.threadworker.submit(btn_pressed, parent, self.inp.get()))
        self.get_btn.grid(row=0,column=2)


class CurrentWeatherFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self['bg'] = '#CCCCCC'    # to have a bit of contrast with the openweathermap icons

        self.city_lab = tk.Label(self)
        self.city_lab.grid(row=0, column=0, sticky='W')

        self.temp_lab = tk.Label(self)
        self.temp_lab.grid(row=1,column=0, sticky='W')

        self.feels_lab = tk.Label(self)
        self.feels_lab.grid(row=2, column=0, sticky='W')

        self.humid_lab = tk.Label(self)
        self.humid_lab.grid(row=3, column=0, sticky='W')

        self.icon_code = None

        self.icon_label = tk.Label(self)
        self.icon_label.grid(row=0, column=1, rowspan=3)

        self.desc_lab = tk.Label(self)
        self.desc_lab.grid(row=2,column=1, rowspan=2)

        self.wind_speed_lab = tk.Label(self)
        self.wind_speed_lab.grid(row=0, column=2, sticky='E')

        self.clouds_lab = tk.Label(self)
        self.clouds_lab.grid(row=1, column=2, sticky='E')

        self.sunrise_lab = tk.Label(self)
        self.sunrise_lab.grid(row=2, column=2, sticky='E')

        self.sunset_lab = tk.Label(self)
        self.sunset_lab.grid(row=3, column=2, sticky='E')

        # change background color of all child widgets
        for widget in self.children.values():
            widget['bg'] = "#CCCCCC"


class ForecastDailyFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self['bg'] = '#CCCCCC'

        self.forecast_day_list = list()

        for i in range(7):
            self.forecast_day_list.append(ForecastDayFrame(self))
            self.forecast_day_list[i].grid(row=0, column=i)


class ForecastDayFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self['bg'] = '#CCCCCC'

        self.day_label = tk.Label(self, text = "test")
        self.day_label.grid(row=0, column=0)

        self.icon_code = None

        self.icon_label = tk.Label(self)
        self.icon_label.grid(row=1, column=0)

        self.weather_desc_label = tk.Label(self)
        self.weather_desc_label.grid(row=2, column=0)

        self.temp_max_label = tk.Label(self)
        self.temp_max_label.grid(row=3, column=0)

        self.temp_min_label = tk.Label(self)
        self.temp_min_label.grid(row=4, column=0)

        for widget in self.children.values():
            widget['bg'] = "#CCCCCC"
