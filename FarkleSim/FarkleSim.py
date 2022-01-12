from collections import Counter
import random
import time

#Notes:
#
# This is a game theory simulator for the game Farkle. Farkle is a dice rolling game, where players take
# turns rolling dice and removing any pairs, 1s, or 5s, ending when they feel like the risk is no longer
# worth the reward. If their roll contains none of these combinations, the player 
# Farkles, their turn ends, and they lose any points they rolled during that round. 
#Full rules can be found at https://en.wikipedia.org/wiki/Farkle
#
# The questions are, when is it worth it to continue rolling? And when is it worth it to remove dice worth
# potentially lesser amounts? Thats what this is for!
#
# My results: 
# 1. It is optimal to remove any 1 value rolled, assuming you have 4 dice remaining or fewer. This means
# that if your initial roll is a [1,1,2,3,4,6], it is best to pull aside one 1, and leave the second to
# try again with 5 dice. Howvever, if the roll is [1,1,3,4,6] it is best to pull out both 1s, and try your 
# continue with 3 dice.. if you choose to continue
# 
# 2. As 5's are worth less than 1's, 5s should be removed when you have 3 dice remaining or fewer. Unless
# of course you choose not to continue
#
# 3. Continuing: The results of average rolls 
# Starting dice:  1 Average points aquired:  280.539
# Starting dice:  2 Average points aquired:  259.849
# Starting dice:  3 Average points aquired:  305.59
# Starting dice:  4 Average points aquired:  380.09
# Starting dice:  5 Average points aquired:  514.964
# Starting dice:  6 Average points aquired:  773.831
#
# By knowing the average result when you have x number of dice remaining, you know when it is advantageous
# to stop playing, and when it is best to take the risk and continue. For example, if you have > 305 points
# andonly 3 dice remaining, it is best mathematically to keep the points and not take the risk rerolling
# This, however does not take into account that other players may be closing in on victory, so take everything
# in stride and have fun :)
#

#Keep track of overall points and rounds
#used to keep track of average points
TOTAL_POINTS = 0
TOTAL_ROUNDS = 0

#In order to simulate likely points from starting at a different number of dice
#Ex. When is it worth it to continue rolling with 3 dice? Can find an expected number of points etc
STARTING_DICE = 6

#Number of simulations to do
NUM_SIMS = 50000

#Dice remaining for you to automatically take remaining 5s or 1s. Can be modified to optimize rolls
#Ex. A roll is [3, 2, 5, 5] 
#   First, the sim will take the first 5, as it is needed in order for play to continue, leaving [3, 2, 5] 
#   It will then look at the FIVES_DICE.
#   if FIVES_DICE is set to 2 (or lower), the sim will ignore the remaining 5
#   since current dice = 3 and cutoff is 2 ([3, 2, 5]) the second 5 will NOT be taken
#
#   However, if FIVES_DICE is set to 3 (or higher), since current dice = 3, the second 5 will be taken

#Optimal: after 50,000 sims with every combo, optimal is for fives to be 3, and ones to be 5.
FIVES_DICE = 3
ONES_DICE = 4


ONES_SINGLE = 6
TWOS_SINGLE = 6
THREES_SINGLE = 6
FOURS_SINGLE = 6
FIVES_SINGLE = 6
SIXES_SINGLE = 6

#Helper function, finds the 1s and 5s in the group.
#Gets the list of dice, returns the index and quantity of 1s and 5s
def findDice(curDice):
    quant1 = 0 #Default to all 0s
    ind1 = 0
    quant5 = 0
    ind5 = 0
    FINISH_FLAG = 0 #this flag makes sure that the program always knows if any combination of only 1s and 5s
                       #are remaining. This way all dice can be taken, and the rolling can continue

    for i in range(len(curDice)):
        if (1 == curDice[i][0]): #If a 1, sets index/quant
            ind1 = i
            quant1 = curDice[i][1]
        if (5 == curDice[i][0]): #if a 5, sets index/quant
            ind5 = i
            quant5 = curDice[i][1]

    if (len(curDice) == 2 and quant1 > 0 and quant5 > 0):
        FINISH_FLAG = 1 #FINISH_FLAG symbols that all dice can be used, speeding up the process and allowing various FIVES_DICE and ONES_DICE values
    return quant1, ind1, quant5, ind5, FINISH_FLAG


# Calculates how many points the user has made this roll
# Finds any pairs, straights, etc. Then takes the set values into account to see
# if any 1s or 5s should be removed.
# Takes the roll and the number of dice as inputs
# Returns the dice remaining after everything was removed, and the points calculated from the roll
# If no dice were removeed and the user Farkles, returns -1, but the numbeer of points as well
def points(dice, roll):
    
    #pairs = [i for i, count in Counter(roll).items if count > 2]
    parse = Counter(roll)

    #sort the tuples, in order of most occurances to least
    #Allows the code to look for pairs in only the first spot in the array
    curDice = parse.most_common(6)

    #counts the points for the individual roll
    cur_points = 0;
    #flag to check and make sure that SOMETHING has been removed. If 0 at the end, the players turn ends and they Farkle
    RMV_FLAG = 0 

    #----------These combos can only be taken a max of once per roll----------

    #three pairs
    if (len(curDice) == 3 and curDice[2][1] == 2):
        return 0, 1500
    #set of 4, and a pair of 2
    if (len(curDice) == 2 and curDice[0][1] == 4):
        return 0, 1500    
    #straight
    if (len(curDice) == 6 and curDice[5][1] == 1):
        return 0, 2500
    #6 of a kind
    if (curDice[0][1] == 6):
        return 0, 3000
    #two pairs of 3
    if(len(curDice) == 2 and curDice[1][1] == 3):
        return 0, 2500
    #Checks for 5 of a kind
    if(curDice[0][1] == 5):
        cur_points += 2000
        curDice.remove(curDice[0])
        RMV_FLAG = 1
        dice -= 5
    ##checks for 4 of a kind
    elif(curDice[0][1] == 4):
        cur_points += 1000
        curDice.remove(curDice[0])
        RMV_FLAG = 1
        dice -= 4
    #Checks for 3 of a kind, but not 2 pairs of 3 since thats already taken
    elif (curDice[0][1] == 3):
        if(curDice[0][1] == 1): #Ones have a special rule, where 3 = 300 instead of 100
            cur_points += 300
            curDice.remove(curDice[0])
        else: #If not a 1..
            cur_points += curDice[0][1]*100
            curDice.remove(curDice[0])
        dice -= 3 #Remove the dice
        RMV_FLAG = 1    #Signal that rolling can continue, if the player has no more good choices

    #Main loop, will go through and take out any 1s and 5s (if desired/needed)
    while (1):    
        #If all dice are used,m passes back for a new roll
        if(dice == 0):
            return 0, cur_points
        else:
            #Finds the quantities and locations of 1s and 5s. These are all that remain of use to the player,
            #And will continue to loop until the player loses, all dice are used, there are no 1s or 5s, or
            #it is not advantageoud to remove any 1s and 5s
            (quant1, ind1, quant5, ind5, FINISH_FLAG) = findDice(curDice)
            #checks the finish flag. If set, only 1s and 5s remain and the round restarts
            if(FINISH_FLAG == 1):
                cur_points += quant1 * 100
                cur_points += quant5 * 50
                return(0, cur_points)
            #checks for any lone ones
            if(dice <= ONES_DICE and quant1 > 0):
                cur_points += quant1 * 100
                dice -= quant1
                curDice.remove(curDice[ind1])
                RMV_FLAG = 1
            #Checks for any lone 5s. Can change how many values are needed to take 5s
            elif(dice <= FIVES_DICE and quant5 > 0):
                cur_points += quant5 * 50
                dice -= quant5
                curDice.remove(curDice[ind5])
                RMV_FLAG = 1
            #Checks if a 1 is NEEDED. If there is nothing else, one available 1 is taken
            elif(RMV_FLAG == 0 and quant1 > 0):
                if (quant1 > 1):
                    curDice.remove(curDice[ind1]) #Tuples are immutable. Removes the index instead
                    curDice.append([ind1,quant1-1]) #and readds it, but with one less 1  
                else:
                    curDice.remove(curDice[ind1])
                dice -= 1
                cur_points += 100
                RMV_FLAG = 1
            #Checks if a 5 is NEEDED. If there is nothing else, one available 5 is taken
            elif(RMV_FLAG == 0 and quant5 > 0):
                if (quant5 > 1):
                    curDice.remove(curDice[ind5]) #Tuples are immutable. Removes the index instead
                    curDice.append([ind1,quant5-1]) #and readds it, but with one less 5  
                else:
                    curDice.remove(curDice[ind5])
                dice -= 1
                cur_points += 50
                RMV_FLAG = 1
            #Nothing left to remove, passes back the remaining dice and points scored
            elif(RMV_FLAG == 1):
                return dice, cur_points
            #If there is nothing possible to take, the turn ends
            elif(RMV_FLAG == 0):
              #  print("Farkle :(")
                return -1, cur_points


def NewRoll(dice, round_points):
    roll = []
    
    for i in range(dice): # rolls new dice
        roll.append(random.randint(1,6))

    #print(dice , ' dice | roll: ', roll)
    (dice, roll_points) = points(dice, roll)

    round_points += roll_points 

    return dice, round_points

# simulates a players turn
# Will continue to roll until they farkle
def turn():
    global TOTAL_POINTS
    global TOTAL_ROUNDS

    round_points = 0
    dice = STARTING_DICE #Sets preliminary dice to be what is set

    #if dice < 0, then the player Farkled and their turn ends
    while (dice >= 0):
        dice, round_points = NewRoll(dice, round_points)

        #If all dice are used, a new round begins and the player keeps rolling 
        if (dice == 0):
           # print("All dice used! Player continues :)  --  Current points: ", round_points)
            dice = 6

    TOTAL_POINTS += round_points
    TOTAL_ROUNDS += 1

#    print("Round points: ", round_points)


# Can use this to test the different times in which you take the ones and five
# Useful for knowing if you should dice back into your pile or not
def TestCutoff():
    global TOTAL_POINTS
    global TOTAL_ROUNDS

    rdpoints = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]

    for ONES_DICE in range(2,6):    #Continue through each combination of ONES and FIVES to find the optimal set 
        for FIVES_DICE in range(2,6):

            for k in range(NUM_SIMS):
                turn();    

            print(ONES_DICE, ",",FIVES_DICE," |  Total points: ", TOTAL_POINTS, " | Total rounds: ", TOTAL_ROUNDS, " | Average points: ", TOTAL_POINTS/NUM_SIMS)

            rdpoints[ONES_DICE][FIVES_DICE] = TOTAL_POINTS #store this sims points
            TOTAL_POINTS = 0 #Reset for the next sim
            TOTAL_ROUNDS = 0
    #Test finished, print results
    for i in range(2,7):
        for j in range(2,6):
           print(i,",", j," |  Total points: ", TOTAL_POINTS, " | Total rounds: ", TOTAL_ROUNDS, " | Average points: ", rdpoints[i][j]/NUM_SIMS)


# Can use this to test how many points youll earn, on average, when starting from any number of dice
# Useful for if youre not sure if its worth gambling and continueing to play
def TestStarting():
    global TOTAL_POINTS
    global TOTAL_ROUNDS
    global STARTING_DICE

    rdpoints = [0,0,0,0,0,0,0]

    for STARTING_DICE in range(1,7):
        for i in range(NUM_SIMS):
            turn()

        print(STARTING_DICE," |  Total points: ", TOTAL_POINTS, " | Total rounds: ", TOTAL_ROUNDS, " | Average points: ", TOTAL_POINTS/TOTAL_ROUNDS)

        rdpoints[STARTING_DICE] = TOTAL_POINTS #store this sims points
        TOTAL_POINTS = 0 #reset for the next sim
        TOTAL_ROUNDS = 0
    #Test finished, print results
    for i in range(1,7):
        print("Starting dice: ", i, "Average points aquired: ", rdpoints[i]/50000 )

# Just runs for fun!
# Id suggest turning on the print statemenets to see how the game goes
def TestforFun():    
    while(1):
        print("-----------NEW PLAYERS TURN---------------")
        turn()
        time.sleep(.5)


# Which simulation you would like to test
TestStarting()