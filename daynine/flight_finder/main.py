import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
load_dotenv()

class PriceFinder:
    def __init__(self):
        self.kiwiKey =  os.getenv("KIWI_API_KEY")
    
    def auth(self):
        headers = {
            "apikey": self.kiwiKey
        }   
        return headers
    
    def shetty_auth(self):
        sheety_header = {"Authorization": os.getenv("CITY_AUTH"),
                         "Content-Type": "application/json"}
        return sheety_header
    
    def invalid_request(self,bool,error_msg):
        format_json = {
            "search_found":bool,
            "error_msg":error_msg
        }
        return format_json

    def locations(self,city):
        """
        This function coverts city name to city code and it reutrn 
        city code if found else error message
        """
        locations_param = {
        "term":city,
        "locations_type":"city"
        }
        locations_endpoint = "https://api.tequila.kiwi.com/locations/query"
        response = requests.get(url=locations_endpoint,headers=self.auth(),params=locations_param)
        print("Locations API reponse code: ",response.status_code)
        response = response.json()
        if response["locations"][0]["name"].lower() == city.lower():
            return response["locations"][0]["code"],True
        else:
            return f"Not found code for {city}",False

    def priceCheck(self,city):
        # all filters for flight finder
        trip_duration = input("How much hours max trips? ")
        max_stopovers = input("How much max stopovers? ")
        city_tuple = self.locations(city)
        if city_tuple[1]:
            city_code = city_tuple[0]
        else:
            error_msg = f"Could not found any city named {city}"
            return self.invalid_request(False,error_msg)
        price_param = {
        "fly_from": "NYC",
        "fly_to": city_code,
        "max_fly_duration":trip_duration,  
        "date_from":"05/12/2023",
        "date_to":"10/12/2023",     
        "return_from":"25/01/2024",
        "return_to":"30/01/2024",
        "selected_cabins":"M",
        "max_stopovers":max_stopovers,
        "curr":"USD"
        }

        url = "https://api.tequila.kiwi.com/v2/search"
        response = requests.get(url=url,headers=self.auth(),params=price_param)
        print("Search API response code: ",response.status_code)
        response = response.json()

        with open(f"daynine/flight_finder/{city}_prices.json","w+") as write_file:
            json.dump(response,write_file,indent=4)

        if response["_results"]!=0:
            response_city_dept = response["data"][0]["cityCodeFrom"]
            response_city_arr = response["data"][0]["cityCodeTo"]
            if price_param["fly_from"] == response_city_dept and price_param["fly_to"] == response_city_arr:
                convert_dt = lambda date_str: datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')

                dept_air = response["data"][0]["flyFrom"]
                arr_air = response["data"][0]["flyTo"]
                dept_time = response["data"][0]["local_departure"]
                arr_time = response["data"][0]["local_arrival"]
                hrs_dept = response["data"][0]["duration"]["departure"]
                hrs_ret = response["data"][0]["duration"]["return"]
                price = response["data"][0]["price"]
                airlines = response["data"][0]["airlines"]
                route = response["data"][0]["route"]
                route_tuple = [(i["cityFrom"],i["cityTo"]) for i in route]

                details = {
                    "search_found":True,
                    "queryDate": datetime.now().strftime("%y/%m/%d"),
                    "queryTime": datetime.now().strftime("%H:%M:%S"),
                    "deptAirport": dept_air,
                    "arrAirport": arr_air,
                    "localDeparture": convert_dt(dept_time),
                    "localArrival": convert_dt(arr_time),
                    "deptHours": round(hrs_dept/3600,2),
                    "arrHours": round(hrs_ret/3600,2),
                    "fare": price,
                    "airlines": str(airlines),
                    "route": str(route_tuple)
                    }

                with open(f"daynine/flight_finder/{city}_details.json","w+") as processed_file:
                    json.dump(details,processed_file,indent=4)
                print("parsing completed")
            else:
                error_msg = f"flights found for {response_city_dept} to {response_city_arr} error in api response"
                return self.invalid_request(False,error_msg)
        else:
            error_msg=f"Could not find any flights for given {trip_duration} hours and {max_stopovers} stop overs! Try again."
            return self.invalid_request(False,error_msg)
        
        return details
    
    def addGoogleSheet(self,city):
        body = {
            "sheet1": self.priceCheck(city)
        }
        if body["sheet1"]["search_found"]:
            postUrl = "https://api.sheety.co/d505e4aa374085caa6ccc710947acf9f/flightPriceTracker/sheet1"
            response = requests.post(url=postUrl,headers = self.shetty_auth(),data=json.dumps(body))
            print("Google sheet api code: ",response.status_code)
            print(json.dumps(response.json(),indent=4))
        else:
            return body["sheet1"]["error_msg"]

bom_prices = PriceFinder()

print(bom_prices.addGoogleSheet("Mumbai"))