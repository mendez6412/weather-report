import requests
import requests_mock
import json
from secrets import API_KEY

with open('durham.json', 'r') as json_data:
    weather_durham = json.load(json_data)

# session = requests.Session()
# adapter = requests_mock.Adapter()
# session.mount('mock', adapter)
# adapter.register_uri('GET', 'mock://test.com', text=weather_durham)
# resp = session.get('mock://test.com')


class Weather():
    def __init__(self, zipcode):
        self.zipcode = zipcode
        self.result = None

    def lookup(self, test=None):
        # conditions/forecast10day/astronomy/alerts/currenthurricane
        if test != None:
            print("TEST")
            self.result = weather_durham
            return weather_durham
        else:
            r = requests.get('http://api.wunderground.com/api/{}/conditions/forecast10day/astronomy/alerts/currenthurricane/q/{}.json'.format(API_KEY, self.zipcode))
            self.result = r.json()
            return(r.json())

    def parse_data(self):
        self.city = self.result['current_observation']['display_location']['city']
        self.state = self.result['current_observation']['display_location']['state']
        self.elevation = self.result['current_observation']['display_location']['elevation']
        self.current_temp = self.result['current_observation']['temp_f']
        self.feelslike = self.result['current_observation']['feelslike_f']
        self.current_uv = self.result['current_observation']['UV']
        self.tenday = []
        for day in self.result['forecast']['simpleforecast']['forecastday']:
            self.tenday.append(("Date: " + day['date']['pretty'],
                                " Conditions: " + day['conditions'],
                                " High Temp: " + day['high']['fahrenheit'],
                                " Low Temp: " + day['low']['fahrenheit']))
        self.sunrise = self.result['moon_phase']['sunrise']['hour'] + ":" + self.result['moon_phase']['sunrise']['minute']
        self.sunset = self.result['moon_phase']['sunset']['hour'] + ":" + self.result['moon_phase']['sunset']['minute']
        self.alerts = self.result['alerts']
        self.hurricanes = []
        for cane in self.result['currenthurricane']:
            self.hurricanes.append(('Name: ' + cane['stormInfo']['stormName_Nice'],
                                    ' Latitute: ' + str(cane['Current']['lat']),
                                    ' Longitude: ' + str(cane['Current']['lon']),
                                    ' Category: ' + cane['Current']['Category']))

    def __str__(self):
        basic = "Location: {}, {}\nTemperature in Fahrenheit: {}\n".format(self.city, self.state, self.current_temp)
        tenday_string = "Ten Day Forecast:\n"
        for day in self.tenday:
            for detail in day:
                tenday_string += (detail + "\n")
        sun = "Sunrise: {}\nSunset: {}\n".format(self.sunrise, self.sunset)
        alerts = ""
        if len(self.alerts) != 0:
            alerts + self.alerts
        else:
            alerts += "NO ACTIVE ALERTS\n"
        hurricanes = "Active Hurricanes:\n"
        if len(self.hurricanes) != 0:
            for cane in self.hurricanes:
                for detail in cane:
                    hurricanes += (detail + "\n")
        else:
            hurricanes += "NO ACTIVE HURRICANES\n"

        return basic + tenday_string + sun + alerts + hurricanes


def main():
    zipcode = int(input("Search by Zip: "))
    q = Weather(zipcode)
    q.lookup()
    q.parse_data()
    print(q)


if __name__ == "__main__":
    main()
