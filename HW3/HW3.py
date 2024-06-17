! pip install openmeteo-requests

import openmeteo_requests
import datetime
import time
from time import mktime
from datetime import datetime


class IncreaseSpeed():
  '''
  Iterator for increasing the speed with the default step of 10 km/h
  You can implement this one after Iterators FP topic

  Constructor params:
    current_speed: a value to start with, km/h
    max_speed: a maximum possible value, km/h

  Make sure your iterator is not exceeding the maximum allowed value
  '''

  def __init__(self, current_speed: int, max_speed: int, step=10):
    self.current_speed = current_speed
    self.max_speed = max_speed
    self.step = step

  def __iter__(self):
    return self

  def __next__(self):
    if (self.current_speed + self.step) <= self.max_speed:
        self.current_speed += self.step
        return self.current_speed
    raise StopIteration


class DecreaseSpeed():
  '''
  Iterator for decreasing the speed with the default step of 10 km/h
  You can implement this one after Iterators FP topic

  Constructor params:
    current_speed: a value to start with, km/h

  Make sure your iterator is not going below zero
  '''

  def __init__(self, current_speed: int, min_speed=0, step=10):
    self.current_speed = current_speed
    self.min_speed = min_speed
    self.step = step

  def __iter__(self):
    return self

  def __next__(self):
    if self.current_speed >= (self.min_speed + self.step):
        self.current_speed -= self.step
        return self.current_speed
    raise StopIteration



class Car():

  '''
  Car class.
  Has a class variable for counting total amount of cars on the road (increased by 1 upon instance initialization).

  Constructor params:
    max_speed: a maximum possible speed, km/h
    current_speed: current speed, km/h (0 by default)
    state: reflects if the Car is in the parking or on the road

  Methods:
    accelerate: increases the speed using IncreaseSpeed() iterator either once or gradually to the upper_border
    brake: decreases the speed using DecreaseSpeed() iterator either once or gradually to the lower_border
    parking: if the Car is not already in the parking, removes the Car from the road
    total_cars: show the total amount of cars on the road
    show_weather: shows the current weather conditions
  '''

  TOTAL_CARS = 0

  def __init__(self, max_speed: int, state, current_speed=0):
    self.current_speed = current_speed
    self.max_speed = max_speed
    self._state = state  # Use _state for private attribute
    if self._state == 'on the road':
        Car.TOTAL_CARS += 1


  @property
  def state(self):
    return self._state


  @state.setter
  def state(self, new_state):
    if new_state not in ("on the road", "in the parking"):
      raise ValueError('Invalid state. Allowed values are "on the road" or "in the parking".')
    self._state = new_state


  def accelerate(self, upper_border=None, step=10):
    # check for state
    # create an instance of IncreaseSpeed iterator
    # check if smth passed to upper_border and if it is valid speed value
    # if True, increase the speed gradually iterating over your increaser until upper_border is met
    # print a message at each speed increase
    # else increase the speed once
    # return the message with current speed

    if self._state == "on the road":
        if upper_border is None and (self.current_speed + step) < self.max_speed:
            self.current_speed += step
            print("Speed increased by ", step)
            print("Current speed is ", self.current_speed)
        elif 0 < upper_border <= self.max_speed:
            speed_increaser = IncreaseSpeed(self.current_speed, upper_border, step)
            for speed in speed_increaser:
                self.current_speed = speed
                print("Speed increased by ",  step)
                print("Current speed is ", self.current_speed)

        elif upper_border >= self.max_speed:
            raise ValueError('Upper border cannot be larger then max speed.')
        elif upper_border < 0:
            raise ValueError('Upper border cannot be less then 0')
    else:
        print("Car is in the parking.")


  def brake(self, lower_border=None, step=10):
    # create an instance of DecreaseSpeed iterator
    # check if smth passed to lower_border and if it is valid speed value
    # if True, decrease the speed gradually iterating over your decreaser until lower_border is met
    # print a message at each speed decrease
    # else increase the speed once
    # return the message with current speed

    if self._state == "on the road":
        if lower_border is None and self.current_speed >= step:
            self.current_speed -= step
            print("Speed decreased by ", step)
            print("Current speed is ", self.current_speed)
        elif lower_border >= 0:
            speed_decreaser = DecreaseSpeed(self.current_speed, lower_border, step)
            for speed in speed_decreaser:
                self.current_speed = speed
                print("Speed decreased by ", step)
                print("Current speed is ", self.current_speed)
        elif lower_border < 0:
            raise ValueError('Lower border cannot be less then 0')
    else:
        print("Car is in the parking.")

  # the next three functions you have to define yourself
  # one of the is class method, one - static and one - regular method (not necessarily in this order, it's for you to think)


  def parking(self):
    # gets car off the road (use state and class variable)
    # check: should not be able to move the car off the road if it's not there

    if self.state == "on the road":
        self.state = "in the parking"
        Car.TOTAL_CARS -= 1
        print("Car parked.")
    else:
        print("Car is already in the parking.")


  @classmethod
  def total_cars(cls):
    # displays total amount of cars on the road

    print(f"Number of cars on the road: {cls.TOTAL_CARS}")


  @staticmethod
  def show_weather():
    # displays weather conditions

    openmeteo = openmeteo_requests.Client()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    "latitude": 59.9386, # for St.Petersburg
    "longitude": 30.3141, # for St.Petersburg
    "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
    "wind_speed_unit": "ms",
    "timezone": "Europe/Moscow"
    }

    response = openmeteo.weather_api(url, params=params)[0]

    # The order of variables needs to be the same as requested in params->current!
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_rain = current.Variables(2).Value()
    current_wind_speed_10m = current.Variables(3).Value()

    print(f"Current time: {datetime.fromtimestamp(current.Time()+response.UtcOffsetSeconds())} {response.TimezoneAbbreviation().decode()}")
    print(f"Current temperature: {round(current_temperature_2m, 0)} C")
    print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
    print(f"Current rain: {current_rain} mm")
    print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")


# Example usage:

test_car_1 = Car(max_speed=70, state="on the road", current_speed=20)
test_car_2 = Car(max_speed=110, state="in the parking")
test_car_3 = Car(max_speed=200, state="on the road", current_speed=170)

test_car_1.accelerate(60)
print("---")
test_car_2.accelerate()
print("---")
test_car_3.accelerate(None, 25)
print("Speed from test_car_3.current_speed: ", test_car_3.current_speed)

# Output:
# Speed increased by  10
# Current speed is  30
# Speed increased by  10
# Current speed is  40
# Speed increased by  10
# Current speed is  50
# Speed increased by  10
# Current speed is  60
# ---
# Car is in the parking.
# ---
# Speed increased by  25
# Current speed is  195
# Speed from test_car_3.current_speed:  195


test_car_1.brake(None, 2)
print("---")
test_car_3.brake(140)

# Output:
# Speed decreased by  2
# Current speed is  58
# ---
# Speed decreased by  10
# Current speed is  185
# Speed decreased by  10
# Current speed is  175
# Speed decreased by  10
# Current speed is  165
# Speed decreased by  10
# Current speed is  155
# Speed decreased by  10
# Current speed is  145


test_car_1.total_cars()
test_car_3.parking()
test_car_1.total_cars()

# Output:
# Number of cars on the road: 2
# Car parked.
# Number of cars on the road: 1


Car.show_weather()
Car.parking()

# Output:
# Current time: 2024-06-17 20:00:00 MSK
# Current temperature: 24.0 C
# Current apparent_temperature: 24.0 C
# Current rain: 0.0 mm
# Current wind_speed: 2.4 m/s

# TypeError: Car.parking() missing 1 required positional argument: 'self'
