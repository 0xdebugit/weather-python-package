from main import cloud_weather
w = cloud_weather('mumbai')
k = w.basic_observation()
a = w.forecast()
x = w.hourly()
print(k)
print(a)
print(x)