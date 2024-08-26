# # import csv
# # with open("weather_data.csv") as weather_file:
# #     data = csv.reader(weather_file)
# #     print(data)
# #     for d in data:
# #         print(d)
#
# # import pandas
# #
# # data = pandas.read_csv("weather_data.csv")
# # day = data[data.temp == "Monday"]
# # temp = day.tem
# import pandas
#
# my_dict = {
#     "record1": {"name": "John", "age": 30, "city": "New York"},
#     "record2": {"name": "Jane", "age": 25, "city": "London"},
#     "record3": {"name": "Mike", "age": 35, "city": "Paris"},
#     "record4": {"name": "Emily", "age": 28, "city": "Sydney"},
#     "record5": {"name": "David", "age": 32, "city": "Tokyo"},
#     "record6": {"name": "Sarah", "age": 27, "city": "Berlin"},
#     "record7": {"name": "Alex", "age": 31, "city": "Toronto"},
#     "record8": {"name": "Emma", "age": 29, "city": "Madrid"},
#     "record9": {"name": "Daniel", "age": 33, "city": "Rome"},
#     "record10": {"name": "Olivia", "age": 26, "city": "Moscow"}
# }
#
# # print(my_dict)
#
# # new_dict = {key: value for (key, value) in my_dict.items() if value["age"] >= 30}
#
# new_DF = pandas.DataFrame(my_dict)
# # print(new_DF)
#
# # for(index, row) in new_DF.iterrows():
# #     print(row.record1)
#
# import csv
# import tkinter
#
# # import pandas
# #
# # data = pandas.read_csv("nato_phonetic_alphabet.csv")
# # dataframe = pandas.DataFrame(data)
# # # print(dataframe.letter)
# #
# # dict1 = {print(value.letter) for (key, value) in dataframe.iterrows()}
# # print(dict1)
#
#
# # def funtion(a, **kwargs):
# #     a += kwargs["add"]
# #     a *= kwargs["mul"]
# #     return a
# #
# # print(funtion(4, add=3, mul=5, div=3))
#
# #
# # class car:
# #     def __init__(self, **kwargs):
# #         self.make = kwargs.get("make")
# #         self.model = "Abc"
# #
# #
# # car1 = car()
# # print(car1.make)
#
# from tkinter import *
#
# window = Tk()
# window.title("my fisrt GUI project")
# window.minsize(height=300, width=500)
# button = Button(text="click me")
#
# i = 0
#
#
# def fun():
#     global i, input
#     data = input.get()
#
#     print(data)
#
#     mylabel["text"] = data
#     text.pack()
#
#
# mylabel = tkinter.Label(text="My label")
# mylabel.pack()
# input = Entry(width=20)
# input.pack()
# button = Button(text="Click me")
# button.pack()
# button.config(command=fun)
#
# text = Text(width=10,height=2)
#
# mainloop()

# try:
#     with open("data.txt", "r") as file:
#         data = file.read()
#         print(data)
# except FileNotFoundError as m:
#     print(m)
# else:
#     print("No exception")
# finally:
#     print("at the end")
import json
import pandas

new_data = {
    "as": {
        "email": "123456",
        "name": "Bh",
    }
}
try:
    with open("data.json", "r") as file:
        # json.dump(new_data,file,indent=4)
        data = json.load(file)
        print(data)

except FileNotFoundError:
    with open("data.json", "w") as data_file:
        json.dump(new_data, data_file, indent=4)
else:
    print("hi")

    data.update(new_data)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
        # data = json.load(file)
        # print(data)
finally:
    print("Hello")

#
# import json
# new_data = {
#     "data": {
#         "email": "Bharath",
#         "name": "Bh",
#     }
# }
# try:
#     with open("data.json", "r") as data_file:
#         # Reading old data
#         data = json.load(data_file)
# except FileNotFoundError:
#     with open("data.json", "w") as data_file:
#         json.dump(new_data, data_file, indent=4)
# else:
#     # Updating old data with new data
#     data.update(new_data)
#
#     with open("data.json", "w") as data_file:
#         # Saving updated data
#         json.dump(data, data_file, indent=4)
# finally:
#     print("Hi")
