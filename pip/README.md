# Weather Application 

This is a simple application for web crawling project
For more info visit : https://gitlab.com/0xdebug/cloud-weather

## Get Started

### How to Install

Use the python package manager [pip](https://pip.pypa.io/en/stable/) to install cloud_weather_app.

```
pip install cloud_weather_app
```

### Requirements

- requests
- beautifulsoup4

### Usage

```
from cloud_weather_app import cloud_weather

# Enter the valid Place Name
mumbai = cloud_weather('mumbai')

# Choose relevant forecast type
daily = mumbai.daily()
monthly = mumbai.monthly()
hourly = mumbai.hourly()

```