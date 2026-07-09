# Sources of the hotel data
import json
from urllib import request 


src_cn = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
src_eng = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

# Proccess hotel data and extract to lists
with request.urlopen(src_cn) as response:
        data_cn = json.load(response)

with request.urlopen(src_eng) as response:
        data_eng = json.load(response)

h_list_cn = data_cn["list"]
h_list_eng = data_eng["list"]

# Store required data into dict
hotel_info = {}
for hotel in h_list_cn:
    if hotel["_id"] not in hotel_info:
        hotel_info[hotel["_id"]] = [hotel["旅宿名稱"]]

for hotel in h_list_eng:
    if hotel["_id"] in hotel_info:
        hotel_info[hotel["_id"]] += [hotel["hotel name"], hotel["tel"]]

print(hotel_info)