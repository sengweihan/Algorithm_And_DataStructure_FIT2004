# FIT2004 S2/2021: Assignment 2 - Dynamic Programming
"""
NAME: SENG WEI HAN
STUDENT_ID : 32229070

"""


def count_encounters(target_difficulty, monster_list):
    """
    PURPOSE : THIS FUNCTION WILL TAKES IN 2 ARGUMENTS, THE FIRST ARGUMENTS IS THE TARGET_DIFFICULTY WHICH IS A 
    NON-NEGATIVE INTEGERS AND A MONSTER_LIST WHICH IS A LIST OF TUPLES.EACH TUPLES REPRESENTS A TYPE OF MONSTER.
    THE FIRST VALUE IN EACH TUPLE IS A STRING WHICH IS THE NAME OF THE TYPE OF MONSTER.THE SECOND VALUE IS 
    A POSITIVE INTEGER, REPRESENTING THE DIFFICULTY OF THAT PARTICULAR TYPE OF MONSTER.

    ARGUMENT : TARGET_DIFFICULTY WHICH IS A NON-NEGATIVE INTEGERS AND A MONSTER_LIST WHICH IS A LIST OF TUPLES.

    RETURN : COUNT_ENCOUNTER RETURNS AN INTEGER, WHICH IS THE NUMBER OF DIFFERENT SETS OF MONSTERS WHOSE 
    DIFFICULTIES SUM TO TARGET_DIFFICULTY. A TYPE OF MONSTER MAY BE USED MORE THAN ONCE IN AN ENCOUNTER

    COMPLEXITY : THE COMPLEXITY FOR THIS COUNT_ENCOUNTER FUNCTION IS O(D*M) WHERE D = VALUE OF TARGET_DIFFICULTY
    AND M = LENGTH OF THE MONSTER LIST SINCE IN THIS IMPLEMENTATION , WE GOT 2 FOR LOOPS , THE OUTER LOOP WILL LOOP
    M TIMES AND EACH INNER LOOP WILL FOR D TIMES HENCE, THE TOTAL COMPLEXITY WILL BE O(DM).

    """
    # firstly create a 2D array
    memo_array = [[0]*(target_difficulty+1) for i in range(len(monster_list))]

    # initialized the base case since if the difficulty = 0 meaning that there's only one combination which is no monster
    for i in range(len(monster_list)):
        memo_array[i][0] = 1

    # If the target difficulty > 0 and len(monster_list) > 0
    if target_difficulty > 0 and len(monster_list) > 0:
        for i in range(len(monster_list)):
            for j in range(1, (target_difficulty+1)):
                # If we are at first row , it will first check if j-monster_list[i][1] >= 0 if true
                if i == 0 and j-monster_list[i][1] >= 0:
                    # then it will take the memo_array[i][subtraction res] to be putted into the memo
                    memo_array[i][j] = memo_array[i][j-monster_list[i][1]]
                else:
                    # if it is less than 0 it will take the optimal result from the row above it.
                    if j-monster_list[i][1] < 0:
                        memo_array[i][j] = memo_array[i-1][j]
                    else:
                        memo_array[i][j] = memo_array[i-1][j] + \
                            memo_array[i][j-monster_list[i][1]]
        return memo_array[len(monster_list)-1][target_difficulty]

    # Handle the case of having an Empty monster list and High Difficulty.
    elif len(monster_list) <= 0 and target_difficulty > 0:
        return 0
    else:  # Handle the case of having Empty Monster List and Zero Difficulty.
        return 1


# target_difficulty = 0
# monster_list = []
# print(count_encounters(target_difficulty, monster_list))

# 2 Greenhouse (18 marks)


def best_lamp_allocation(num_p, num_l, probs):
    """
    PURPOSE : THIS FUNCTION WILL TAKES IN 2 ARGUMENTS AND COMPUTE THE MAXIMUM PROBABILITY THAT ALL PLANTS 
    WILL BE FULLY GROWN BY THE DAY OF THE PARTY GIVEN SOME NUMBER OF LIGHTS.

    ARGUMENTS : NUM_P AND NUM_L ARE POSITIVE INTEGERS REPRESENTING THE NUMBER OF PLANTS AND LAMPS RESPECTIVELY WHEREAS
    PROBS IS A LIST OF LIST WHERE PROB[I][J] REPRESENTS THE PROBABILITY THAT PLANT I WILL BE READY IN TIME IF IT IS ALLOCATED J LAMPS

    RETURN : BEST_LAMP_ALLOCATIONS WILL RETURNS A FLOAT WHICH IS THE HIGHEST PROBABILITY OF ALL PLANTS BEING READY BY THE PARTY 
    THAT CAN BE OBTAINED BY ALLOCATING LAMPS TO PLANTS OPTIMALLY.

    COMPLEXITY : THIS FUNCTIONS RUNS IN O(PL^2) TIME WHERE P = NUM_P AND L = NUM_L

    """

    # create a temp variables to store values for comparison
    temp = 0
   # first create a memo matrix of size (num_p + 1) * (num_l + 1)
    memo_array = [[0] * (num_l+1) for i in range(num_p+1)]
    # print(memo_array)

    # for zero plants the probability will all be 1 no matter how many lights provided to them.
    for a in range(len(memo_array[0])):
        memo_array[0][a] = 1

    # update the memo for the case where there's 0 lamp
    for b in range(1, len(memo_array)):
        memo_array[b][0] = probs[b-1][0] * memo_array[b-1][0]

    # loop through the row for the plant in the memo_array.
    for i in range(1, len(memo_array)):
        # loop through the columns for the lamps of the memo_array.
        for j in range(1, len(memo_array[i])):
            # k will be the column part for the previous row.
            for k in range(j+1):
                temp = memo_array[i-1][k] * probs[i-1][j-k]

                if temp > memo_array[i][j]:
                    memo_array[i][j] = temp

                if k == j:
                    if memo_array[i][j-1] > memo_array[i][j]:
                        memo_array[i][j] = memo_array[i][j-1]
    # print(memo_array)

    return memo_array[num_p][num_l]
