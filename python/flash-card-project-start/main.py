# BACKGROUND_COLOR = "#B1DDC6"
#
# import pandas
#
#
# data = pandas.read_csv("data/french_words.csv")
# dict = data.to_dict(orient="records")
# print(dict)

import requests

response = requests.get(url="http://api.open-notify.org/iss-now.json")
print(response.json())
