from pickletools import read_uint1
from flask import request
import requests

class Post:
    
    def blog_locater(self):
        url = "https://api.npoint.io/c790b4d5cab58020d391"
        response = requests.get(url)
        return response.json()
    
