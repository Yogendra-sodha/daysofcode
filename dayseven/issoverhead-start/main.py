import requests
import time
from datetime import datetime

MY_LAT = 36.7201600
MY_LONG = -4.4203400 

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# Sunrise API call
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


# sunset , isslon, isslng, my lng, my long

machine = True
i=0

while machine:
    time.sleep(60)
    time_now = datetime.now()
    current_hour = int(str(time_now).split(" ")[1].split(":")[0])
    if current_hour >= sunset:
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])

        lat_diff = int(iss_latitude - MY_LAT)
        lng_diff = int(iss_longitude - MY_LONG)

        if -5 <= lat_diff <= 5 and -5 <= lng_diff <= 5:
            print("iss Above you")
        else:
            print("Not near you")