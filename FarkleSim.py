
from collections import Counter
import random
import time

#Keep track of overall points and rounds
#used to keep track of average points
TOTAL_POINTS = 0
TOTAL_ROUNDS = 0

#In order to simulate likely points from starting at a different number of dice
#Ex. When is it worth it to continue rolling with 3 dice? Can find an expected number of points etc
STARTING_DICE = 6

#Dice remaining to take a 5. Not an ideal for gaining points possibly, so can be changed
#Ex. if 3, takes 5s when 3 dice remaining or fewer
FIVES_DICE = 3

def points(roll):
    

    #pairs = [i for i, count in Counter(roll).items if count > 2]
    parse = Counter(roll)

    cur = parse.most_common(6)


     #three pairs
    if (len(cur) ==3 and cur[2][1] == 2):
        return 1500
     #set of 4, and a pair of 2
    if (len(cur) ==2 and cur[0][1] == 4):
        return 1500    
    #straight
    if (len(cur) == 6 and cur[5][1] == 1):
        return 2500
    #6 of a kind
    if (cur[0][1] == 6):
        return 3000

    #counts the points for the individual roll
    cur_points = 0;
    #flag to check and make sure that SOMETHING has been removed
    RMV_FLAG = 0 

    while (1):
        #If all dice are used
        if(len(cur) == 0):
            return 0, cur_points
        #Checks for 5 of a kind
        if(cur[0][1] == 5):
            cur_points += 2000
            cur.remove(cur[0])
            RMV_FLAG = 1
        ##checks for 4 of a kind
        elif(cur[0][1] == 4):
            cur_points += 1000
            cur.remove(cur[0])
            RMV_FLAG = 1
        #checks for 3 of a kind
        elif(cur[0][1] == 3):
            if(cur[0][1] == 1):
                cur_points += 300
                cur.remove(cur[0])
            else:
                cur_points += cur[0][1]*100
                cur.remove(cur[0])
            RMV_FLAG = 1
        #checks for any lone ones
        elif(cur.count(1) > 0):
            ind = cur.index(1)
            cur_points += cur[ind][1] * 100
            cur.remove(1)
            RMV_FLAG = 1
        #Checks for any lone 5s. Can change how many values are needed to take 5s
        elif(len(cur) < FIVES_DICE and cur.count(5) > 0):
            ind = cur.index(5)
            cur_points += cur[ind][1] * 50
            cur.remove(5)
            RMV_FLAG = 1
            #Cheks if a 5 is needed
        elif(RMV_FLAG != 1 and cur.count(5) > 0):
            ind = cur.index(5)
            cur_points += cur[ind][1] * 50
            cur.remove(5)
            RMV_FLAG = 1
        elif(RMV_FLAG == 1):
            return len(cur), cur_points
        elif(RMV_FLAG == 0):
            return -1, cur_points


def NewRoll(dice, round_points):
    roll = []
    
    for i in range(dice): # rolls new dice
        roll.append(random.randint(1,6))

    print(dice , ' dice | roll: ', roll)
    (dice, roll_points) = points(roll)

    round_points += roll_points 

    return dice, round_points

#simulates a players turn
def round():
    global TOTAL_POINTS
    global TOTAL_ROUNDS

    round_points = 0
    dice = STARTING_DICE #Sets preliminary dice to be what is set

    #if dice < 0, then the player Farkled and their turn ends
    while (dice >= 0):
        dice, round_points = NewRoll(dice, round_points)

        #If all dice are used, a new round begins and the player keeps rolling 
        if (dice == 0):
            dice = 6

    TOTAL_POINTS += round_points
    TOTAL_ROUNDS += 1

    print("Round points: ", round_points)
    print("Total points: ", TOTAL_POINTS, " | Total rounds: ", TOTAL_ROUNDS, " \ Points per round: ", TOTAL_POINTS/TOTAL_ROUNDS)


if __name__ == "__main__":

    while (1):
        round()
        time.sleep(10)



