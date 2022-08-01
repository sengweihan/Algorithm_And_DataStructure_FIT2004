"""
NAME: SENG WEI HAN
STUDENT_ID : 32229070
"""
import math
import time
import timeit
import random


# QUESTION 1 :INTEGER RADIX SORT


def counting_sort(lst, column_value, base):
    """
    PURPOSE : THIS FUNCTION WILL TAKES IN 3 ARGUMENT AND IT WILL CREATE A COUNT_ARRAY OF SIZE BASE AND LOOP THROUGH THE INPUT LIST AND
    PUT VALUES INTO THE BUCKET BASED ON THE DIGITS OF THAT VALUE USING THE FORMULA : item//(base**column_value) % base 
    ONCE IT IS DONE, IT WILL LOOP THROUGH THE COUNT_ARRAY AND UPDATED BACK ITS VALUE INTO THE INPUT LIST. THIS IMPLEMENTATION WILL 
    MUTATE THE ORIGINAL LIST TO BE THE SORTED LIST AT THE END.

    ARGUMENT : A LIST OF NON-NEGATIVE VALUES, THE COLUMN VALUE FROM RADIX SORT AND ALSO THE BASE.

    RETURN : A SORTED LIST WHICH IS SORTED BASED ON THE DIGIT AT THAT PARTICULAR COLUMN VALUE.

    COMPLEXITY : O(M+N) WHERE M = THE COUNT_ARRAY AND N = INPUT LIST
    """

    # create a count_array which is as big as max
    count_array = [None] * base
    # to maintain stability create a nested list
    for i in range(len(count_array)):
        count_array[i] = []
        # loop through the input lst to get the frequency
    for item in lst:
        # get the index of the item
        index_col = item//(base**column_value) % base
        count_array[index_col].append(item)
    # print(count_array)

    # loop through the count_array to update the new results into input list.
    index = 0
    for row in range(len(count_array)):
        for col in range(len(count_array[row])):
            lst[index] = count_array[row][col]
            index += 1

    # print(lst)
    return lst


def num_rad_sort(num, base):
    """
    PURPOSE : Basically what this function does is, it will take 2 argument which is the base and the integer list. Then , it will sort the integer
    list by calling counting sort multiple times based on the number of digits of the largest value.Instead of sorting by value, this function
    will sort those value by digits.

    ARGUMENT :  nums is a unsorted list of non-negative integers and b is an integer, with value ≥ 2.

    RETURN : a sorted list of non-negative integers.

    COMPLEXITY : O(N+M) * O(log (base) M) 

    """

    # find the max in input lst to determine the number of digits
    maximum = num[0]
    for i in range(1, len(num)):  # COMPLEXITY = O(N)
        if maximum < num[i]:
            maximum = num[i]

    # Obtain the number of digit of greater value by using len()
    # num_of_digits = len(str(maximum))  # num of column
    num_of_digits = (math.floor(math.log(maximum, base)+1)
                     )  # COMPLEXITY = O(1)

    # loop through each column
    # this for loop will loop for k times where k = num of digits
    for col in range(num_of_digits):

        num = counting_sort(num, col, base)

    return num


# QUESTION 2 : BASE TIMING
def base_timer(num_list, base_list):
    """
    PURPOSE : THE PURPOSE OF THIS FUNCTION IS TO INVESTIGATE THE RELATIONSHIP BETWEEN THE BASE USED AND THE RUN-TIME

    ARGUMENT : A NUM LIST CONSISTING OF NON-NEGATIVE INTEGERS AND A BASE LIST.

    RETURN: A LIST CONSISTING OF RUN-TIMES .
    """
    # created an empty list to obtained those run-time from each iteration.
    lst = []
    for item in base_list:
        start = time.time()
        # code you want to time
        num_rad_sort(num_list, item)
        time_taken = time.time() - start
        lst.append(time_taken)

    return lst


# QUESTION 3 : INTEREST GROUP

def radix_sort_string(lst):
    """
    PURPOSE : THIS FUNCTION BASICALLY DOES THE SAME THING AS THE NUM_RAD_SORT WE IMPLEMENTED EARLIER BUT THE DIFFERENCE BETWEEN NUM_RAD_SORT
    AND THIS FUNCTION IS , THIS FUNCTION IS USED TO SORT STRINGS INSTEAD OF INTEGERS.

    ARGUMENT : A LIST OF LOWER-CASE STRINGS 

    RETURN : A SORTED LIST OF LOWER-CASE STRINGS.

    COMPLEXITY : O(k) * O(N+M) WHERE K = COL VALUE, N = LENGTH OF INPUT STRING LIST AND M = LENGTH OF COUNT_ARRAY.
    """
   # lst = ['cat', 'taco', 'tags', 'gitgud', 'gudetama', 'food']

    max = len(lst[0])

    for i in range(len(lst)):
        if max < len(lst[i]):
            max = len(lst[i])
    # print(max)

    for col in range(max-1, -1, -1):  # start from bottom to top
        lst = counting_sort_string(lst, col)

    return lst


def counting_sort_string(lst, col):
    """
    PURPOSE : THIS FUNCTION WILL RECEIVE A LIST OF STRINGS AND THE COLUMN VALUE TAKEN FROM RADIX_SORT_STRING AND INITIALIZED A COUNT_ARRAY
    WTIH 27 SLOTS WHERE THE FIRST SLOT IS USED TO APPEND ITEMS WHEN THE LEN(ITEM) <= COL AND LASTLY WILL RETURN A SORTED LIST OF STRINGS 

    ARGUMENT : A LIST OF UNSORTED STRINGS AND THE COLUMN VALUE TAKEN FROM RADIX_SORT_STRING.

    RETURN : A SORTED LIST OF STRINGS 

    COMPLEXITY : O(N+M) WHERE N = LENGTH OF INPUT LIST OF STRINGS AND M = SIZE OF COUNT_ARRAY WHICH IN THIS CASE IS CONSTANT WHICH IS 27.
    """
    # initialized a count array with 27 slot (indicate from a(1) to z(26))
    count_array = [None] * 27

    for i in range(len(count_array)):
        count_array[i] = []

    for item in lst:
        if len(item) <= col:
            count_array[0].append(item)
        else:
            index = ord(item[col]) - 96
            if index < 0:
                count_array[0].append(item)
            else:
                count_array[index].append(item)

    # print(count_array)

    index = 0
    for row in range(len(count_array)):
        for col in range(len(count_array[row])):
            lst[index] = count_array[row][col]
            index += 1

    # print(lst)

    return lst


def counting_sort_lst(lst):
    """
    PURPOSE : THIS IS AN ADDITIONAL FUNCTION WHICH I HAVE CREATED IN ORDER TO SORT A LIST OF LIST 

    INPUT : A LIST OF LIST

    OUTPUT : A SORTED LIST OF LIST 

    COMPLEXITY : O(N+M) WHERE N = LENGTH OF INPUT LIST AND M = LENGTH OF COUNT_ARRAY.
    """
    # create a new count_array based on the length of the input list.
    n = len(lst)

    count_array = [None] * (n+1)

    for i in range(len(count_array)):
        count_array[i] = []

    for item in lst:
        size = len(item)
        count_array[size].append(item)

    index = 0
    for row in range(len(count_array)):
        for col in range(len(count_array[row])):
            lst[index] = count_array[row][col]
            index += 1

    return lst


def interest_groups(data):
    """
    PURPOSE : THE MAIN PURPOSE OF THIS FUNCTION IS TO CREATE(GROUP THEM TOGETHER) A GROUPS OF PEOPLE WITH IDENTICAL INTEREST.

    INPUT : data is a list, where each element is a 2-element tuple representing a person. The first element
           is their name, which is a nonempty string of lowercase a-z with no spaces or punctuation. Every
           name in the list is unique.The second element is a nonempty list of nonempty strings, which represents the things this
           person likes. The strings consist of lowercase a-z and also spaces (i.e. they can be multiple
           words) but no other characters. This list is in no particular order.


    OUTPUT: interest_groups returns a list of lists. For each distinct set of liked things, there is a list
           which contains all the names of the people who like exactly those things. Within each list,
           the names should appear in ascending alphabetical order. The lists may appear in any
            order.

    COMPLEXITY : O(NM)
    """
    lst = []
    lst_interest = []
    lst_people = []

    # loop through the input data and take list of interest and use radix_sort_string to sort the interest list then it will put
    # the sorted interest list to the position of i in data to replace the unsorted version of the interest list.
    for i in range(len(data)):
        name = data[i][0]
        tup = data[i][1]
        new_lst = radix_sort_string(tup)
        # put the results returned from radix sort into the data .
        data[i] = (name, new_lst)
        lst.append(new_lst)

    # this new _list is sorted based on length of list.
    new_lst = counting_sort_lst(lst)

    # grouping them and remove duplicates.
    for i in range(len(new_lst)):
        if new_lst[i] not in lst_interest:
            lst_interest.append(new_lst[i])

    # create a list of sublist based on the value of n
    n = len(lst_interest)
    for i in range(n):
        lst_people.append([])

    # LOOP THROUGH THE LIST INTEREST AS OUTER LOOP AND THE MODIFIED DATA LIST AS INPUT LIST AND COMPARE BETWEEN THE LIST OF INTEREST IN DATA
    # AND THE LIST IN THE LST_INTEREST , IF BOTH OF THEM MATCHES MEANING TO SAY THAT THE NAME OF THE PEOPLE IN DATA[J][0] WILL BE
    # THE ONE WE WANTED TO APPEND INTO THE SUBLIST OF LST_PEOPLE.

    for i in range(len(lst_interest)):
        for j in range(len(data)):
            if data[j][1] == lst_interest[i]:
                lst_people[i].append(data[j][0])

    # finally we will need to sort each of the lst_people in alphabetical order.
    for i in range(len(lst_people)):
        lst_people[i] = radix_sort_string(lst_people[i])

    return lst_people


if __name__ == "__main__":
    random.seed("FIT2004S22021")
    data1 = [random.randint(0, 2**25) for _ in range(2**15)]
    data2 = [random.randint(0, 2**25) for _ in range(2**16)]
    bases1 = [2**i for i in range(1, 23)]
    bases2 = [2*10**6 + (5*10**5)*i for i in range(1, 10)]
    y1 = base_timer(data1, bases1)
    y2 = base_timer(data2, bases1)
    y3 = base_timer(data1, bases2)
    y4 = base_timer(data2, bases2)
