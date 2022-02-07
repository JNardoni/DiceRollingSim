# FarkleRollingSim
Simulates best course of action for the game Farkle

Farkle is a dice rolling game, where players take turns rolling dice and removing any pairs, 1s, or 5s, 
ending when they feel like the risk is no longer worth the reward. If their roll contains none of these 
combinations, the player Farkles, their turn ends, and they lose any points they rolled during that round. 

Full rules can be found at https://en.wikipedia.org/wiki/Farkle

# Using the sim

The simulation has a few different testing functions, each checking a different variable in an attempt to optimize
the players rolling, tell them when to stop and when to continue. They are,

1. TestPairsCutoff: This is used to determine when it is best to take pairs, and when it is best to leave them.
For example, if three 2s are rolled, is it worth it to take them? Or to pull aside a single 1 or 5 in order to have more dice in 
the next roll?

2. TestSingleCutoff: This is used to track when a 1 or 5 should be taken. With larger rolls, is it best to take extra 1s and 5s, 
or leave them so that your next roll has more dice?

3. TestStartingDice: This tests the average points you will get if you continue to roll until you Farkle with each number of starting
dice. By using the averages, you can determine if its worth it to continue rolling. If your current score is below the average for that
many dice rolled, you have more to gain than to lose if you were to keep going.

4. TestCurrentConfig: This tests the current setup, the combination of the three variables mentioned above

# My Results

1. TestPairsCutoff<br />
For triples, 1s and 3s are worth the same (300 points). Any triples of 1s or 3s should be taken 4 dice remaining. For ex. <br/>
If a roll is [3,3,3,1,4,6], more than 4 dice remain which means the 1 should be taken. Since five dice remain, the triple 3s 
are not worth taking for the roller, and they should roll with 5 dice instead. If the roll was [3,3,3,1,6] however, the 1 would still 
be taken, and as 4 dice now remain, the triple 3s should then be taken to optimize points.<br/>
2s are worth less than 1s and 3s, and also worth less than rolling single 1s in consecutive rolls. As they earn minimal points,
they should be taken only to complete the roll. 4s, 5s, and 6s are worth farm more points and should always be taken.


2. TestSingleCutoff<br />
It is optimal to remove any 1 value rolled if you have 4 dice remaining or fewer (including that 1). This means
that if your initial roll is a [1,1,2,3,4,6], it is best to pull aside one 1, and leave the second to
try again with 5 dice. Howvever, if the roll is [1,1,3,4,6] it is best to pull out both 1s, and 
continue with 3 dice.. if you choose to try your luck, that is. <br /> As 5's are worth less than 1's, 5s should be removed when you have 3 dice remaining or fewer. Unless of course you choose not to continue,
in which case as many dice as possible should be taken


3. TestStartingDice<br />
    Starting dice:  1 |  Average points aquired:  305.462 <br />
    Starting dice:  2 |  Average points aquired:  245.926 <br /> 
    Starting dice:  3 |  Average points aquired:  321.848  <br />
    Starting dice:  4 |  Average points aquired:  411.313  <br />
    Starting dice:  5 |  Average points aquired:  542.185  <br />
    Starting dice:  6 |  Average points aquired:  841.255


