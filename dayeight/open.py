import requests
my_lat = 51.507351
my_lon = -0.127758
app = "62d96c0b499e342532d908723547cd33"

param = {
    "lat":my_lat,
    "lon":my_lon,
    "appid": app
}

response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={my_lat}&lon={my_lon}&appid={app}")
response.raise_for_status()

print(response.json())