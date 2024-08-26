# print("hello \"Bharath\" \n hello \"Bharath\"")
# print("hello \"Bharath\"" +"How are you")
# # print("hello \"Bharath\"")
# # print("hello \"Bharath\"")

# print("Hello " + input("enter your name"))
# num1 = int(input())
# num2 =input()
# num3 = num1*num2
# print(num3)

# print(1_23_456)

# length =len(input("enter name"))
# print("Length" + str(length))
# print( type(length))


# a =100
# b=100
# print(a+str(b))

# a =77
# print(a%10 + a%100)
# print(int(str(a)[0])+int(str(a)[1]))


# BMI cal
# round off function

# weight =float(input())
# height = float(input())
# height =height**2
# BMI=weight/height
# print(round(BMI,2))

# floor division
# print(9//3)

# sum = 0
# sum += 1
# print(sum)

# F-String

# sum=100;
# print(f"sum is {sum}")

# age=int(input())
# remaining_yrs =90-age
# Noofweeksleft =remaining_yrs*364//7
# print(f"Total {Noofweeksleft} are left")

# formating
# sum =90.0
# sum = "{:.5f}".format(sum)
# print(f"round off to 2 digits {sum}")

# Conditional operators

# If-else

# sum =20
# if sum>=60:
#     print("it's greater than or equals to 60")
# else:
#     print(f"{sum} less than 60")

# even odd

# num =61

# if num%2==0:
#     print("even")
# else:
#     print("odd")

# leap year

# year =1704
# if year%4==0:
#     if year%100 ==0:
#         if year %400 ==0:
#             print(f"{year} is a leap year")
#         else:
#             print(f"{year} is a not leap year")
#     else:
#         print(f"{year} is a leap year")

# Count

# name ="Bharath"
# count =name.count("a")
# print(count)


# Random numbers

# import random
# import pi


# num =random.seed()
# print(num)


# List

# names=["bha","asd","bha","bha","asd","bha","asd","bha","asd"]

# for n in names:
#     print(n)


# for

# for i in range(0,10):
#     print(i)


# def myfun():
#     print("who are you")
# myfun()


# def my_function():
#          print("Hello")
# print("bye")
# my_function()
# import random
# words =["Bharath","asdf","qwert","zxcv"]

# choice =random.choice(words)


# c =choice.find('a')

# print(choice)
# print(c)

# functions with the parameters
# a = (1, 2, 3, 4, 5)
# x = sum(a, 7)
# print(x)
# def myfun(name,num):
#     print(name)
#     c=len(name)
#     print(c)

#     a =9+num
#     print(f"{a}")

# myfun(name=99,num="bha")


# Round up
# import math
# def cal(width,height,cov):
#     area =width*height
#     buc=area/cov
#     tota=math.ceil(buc)
#     print(tota)


# width =int(input())
# height =int(input())
# coverage =5
# cal(width=width,height=height,cov=coverage)

# Prime number

# def primeornot(num):
#     """ Prime """
#     isprime=False
#     i=2
#     while i!=num:
#         if num%i ==0:
#             isprime=True
#         i+=1

#     def primeornot(num):
    
#         isprime=False
#         i=2
#         while i!=num:
#             if num%i ==0:
#                 isprime=True
#             i+=1
        
#         print(f"{num} is a primenumber: {not isprime}")
    
#     print(f"{num} is a primenumber: {not isprime}")
    

# num =int(input())
# primeornot()


# student_scores = {"Harry": 81, "Ron": 78,
#                   "Hermione": 99,
#                   "Draco": 98,
#                   "Draco": 74,
#                   "Neville": 62}
    
# student_grades={}
# for key in student_scores:
#     if student_scores[key]>90:
#         student_grades[key]="O"
#     elif student_scores[key]>80:
#         student_grades[key]="EE"
#     elif student_scores[key]>70:
#         student_grades[key]="A"
#     else:
#         student_grades[key]="F"

# student_scores[1]=2
# print(student_scores)


# print(student_scores)
# # print(student_grades)

# student_scores



# def add(i,j):
#     return i+j
# dict={
#     "a":add
# }
# a =int(input())
# b=int(input())
# c="add"

# print(c(a,b))

#Schope

n=1
def function():
    global n
    n+=1
    print(f"Vales of n inside the function {n}")

function()

print(f"Vales of n outside the function {n}")