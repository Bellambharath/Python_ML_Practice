# #Capstorn
# import math,random

# def winorlose(cards,computer,user):
#     highestscore= max(sum(computer),sum(user))
#     if highestscore>=21:
#         if(highestscore==21):
#             if((sum(computer)==21) and (sum(user)==21)):
#                 print(f"User cards {user}")
#                 print(f"computer cards {computer}")
#                 print("Draw")
#             elif(sum(computer)==21):
#                 print(f"computer cards {computer}")
#                 print("User lose")
#             else:
#                 print(f"User cards {user}")
#                 print("User Win")
#         else:
#             if(sum(computer)>21):
#                 print(f"computer cards {computer}")
#                 print("User win")
#             else:
#                 print(f"User cards {user}")
#                 print("User lose")
#         return

#     else:
#         print(f"User cards {user}")
#         pickcard = input("Do you want to pick another card type y or n \n")
#         if(pickcard.lower()=='y'):
#             selectedcard=random.choice(cards)
#             user.append(selectedcard)
#             winorlose(cards=cards,computer=computer,user=user)

#     print(f"highestscore: {highestscore}")


# cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
# computer=[]
# user=[]
# computer=random.choices(cards,k=2)
# user=random.choices(cards,k=2)
# print(computer)
# print(user)

# if(sum(computer)==21 or sum(user)==21):
#     if(sum(computer)==21):
#         print("Computer got the blackjack,User lose")
#     else:
#         print("user got the blackjack,User win")
# elif(sum(computer)>21 or sum(user)>21):
#     if(sum(computer)>21):
#         index=computer.index(11)
#         computer[index]=1
#     if(sum(user)>21):
#         index=user.index(11)
#         user[index]=1
#     print(f"Computer first card is :{computer[0]}")
#     winorlose(cards=cards,computer=computer,user=user)
# else:
#     print(f"Computer first card is :{computer[0]}")
#     winorlose(cards=cards,computer=computer,user=user)


# Number guessing game
# import random
# number = random.randint(1,100)
# level =input("choose the difficulty level 'easy' or 'hard' \n")
# chances=5
# if(level.lower() =='easy'):
#     chances=10
# else:
#     chances=5
# guess=0
# for c in range(0,chances):

#     guess=int(input(f"you have {chances-c} attempts remaining to guess \n make a guess "))
#     if(guess>number):
#         print("Too High \n  guess again")
#     elif(guess<number):
#         print("Too low \n  guess again")
#     else:
#         print("You got it")
#         break
# if(guess!=number):
#     print("you lossed it , run out of chances")


# HighLow game

import data
import random
import os


terminate = False


def cal(random_account_A, random_account_B, score, choice):
    if (choice.lower() == 'a'):
        if (random_account_A['follower_count'] >= random_account_B['follower_count']):
            score += 1
            os.system('cls')
            print(f"You are right ! Current score is {score}")
            return random_account_B, score, False
        else:
            os.system('cls')

            print(f"Sorry that's wrong your score is {score}")
            return
    else:
        if (random_account_A['follower_count'] < random_account_B['follower_count']):
            score += 1
            os.system('cls')
            print(f"You are right ! Current score is {score}")
            return random_account_B, score, False
        else:
            os.system('cls')
            print(f"Sorry that's wrong your score is {score}")
            return


random_account_A = random.choice(data.data)
score = 0
print(
    f"A:- {random_account_A['name']}, {random_account_A['description']}, from {random_account_A['country']},followers {random_account_A['follower_count']} ")

random_account_B = random.choice(data.data)
print(
    f"B:- {random_account_B['name']}, {random_account_B['description']}, from {random_account_B['country']},followers {random_account_B['follower_count']}")

choice = input("Who has more followers ? Type 'A' or 'B'")
result = cal(random_account_A, random_account_B, score, choice)

print(f"result {result}")
while result !=None:
    # print(result[0])
    print(
    f"A:- {result[0]['name']}, {result[0]['description']}, from {result[0]['country']},followers {result[0]['follower_count']} ")

    random_account_B = random.choice(data.data)
    print(
        f"B:- {random_account_B['name']}, {random_account_B['description']}, from {random_account_B['country']},followers {random_account_B['follower_count']}")
    choice = input("Who has more followers ? Type 'A' or 'B'")
    result = cal(result[0],random_account_B, result[1], choice)
