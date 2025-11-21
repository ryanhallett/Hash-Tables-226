import csv
import random
import math
import time

class DataItem:
    def __init__(self, line):
        self.movie_name = line[0]
        self.genre = line[1]
        self.release_date = line[2]
        self.director = line[3]
        self.revenue = line[4]
        self.rating = line[5]
        self.min_duration = line[6]
        self.production_company = line[7]
        self.quote = line[8]

# create empty hash tables
size = 8192

# Going to use collision for this, so new tables needed
hashTitleTable = [[] for _ in range(size)]
hashQuoteTable = [[] for _ in range(size)]

file = "MOCK_DATA.csv"
counter = 0

# need to reduce the size of my values to fit into pythons system
def conversion(key):
    prime = 31
    reduce = 2**53 - 1
    value = 0
    for char in key:
        # using prime to create randomness
        value = (value * prime + ord(char)) % reduce
    return value

# 5 hash functions - mod, folding, midSquare, universal, multiplication
# pass in the converted value

# keeping it simple
def mod(key):
    # pretty basic modding
    newKey = key % size
    # return the key!
    return newKey

# folding a bit
def fold(key):
    # setting up a list for the folded digits
    # slicing using predetermined size and another list
    slices = 3
    digits = []
    sliced = []

    # if there is still digits in key
    while key > 0:
        # append the last digit to a list
        digits.append(key % 10)
        # divide by 10
        key //= 10

    # reverse the list instead of inserting 
    # inserting is less efficient
    digits.reverse()

    for i in range(0, len(digits), slices):
        sliced.append(digits[i:i + slices])
    
    #return newKey

# doing some wacky math
def midSquare(key):
    # sqaure the key
    square = key * key
    # convert to strings
    str_list = str(square)
    # get the middle
    middle = len(str_list) // 2
    # find the start and end
    start = middle - 2
    end = middle + 3
    # get the middle 5 digits
    middle_five = str_list[start:end]
    # turn it back into an integer and mod
    newKey = int(middle_five) % size
    return newKey

# universally applying??
def universal(key):
    # get a prime (large)
    prime = 9999991
    # select two random numbers
    a = random.randint(1, (prime - 1))
    b = random.randint(0, (prime - 1))
    #multiply randomA(key) + randomB
    value = ((a * key) + b) % prime
    # mod a large prime number,
    # # typically larger than the max possible value 
    # from key, not sure if that will work yet
    # had to get AI to generate a prime for me 
    # finally, mod by size 
    newKey = value % size
    # return newKey
    return newKey

# golden ratio mutiplication
def multiplication(key):
    # the formula said golden ratio was "usually" used
    golden_ratio = float(0.61803398875)
    # find the value, remove the integer, keep the fraction
    # multiply by size
    value = ((key * golden_ratio) % 1) * size
    # round it down
    newKey = math.floor(value)
    return newKey

# chaining because we used lists to create the tables
def handle_collisions(table, index, movie):
    # collision happens when a bucket is not empty
    collision_happened = len(table[index]) > 0
    table[index].append(movie)
    
    if collision_happened == True:
        return 1
    else:
        return 0

def unused_buckets(table):
    unused = 0
    for bucket in table:
        if len(bucket) == 0:
            unused += 1
    return unused

t_collisions = 0
q_collisions = 0

start = time.time()

with open(file, 'r', newline='',  encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # skip header
        if counter == 0:
            counter += 1
            continue

        # create movie from data(row)
        movie = DataItem(row)

        # convert movie title and movie quote to keys (large numbers)
        titleKey = conversion(movie.movie_name)
        quoteKey = conversion(movie.quote)

        # ONE AT A TIME
        # commit after each attempt
        # mod
        #hashKeyT = mod(titleKey)
        #hashKeyQ = mod(quoteKey)

        # fold - NEED TO FIX STILL
        # hashKeyT = fold(titleKey)
        #hashKeyQ = fold(quoteKey)

        # mid Square
        #hashKeyT = midSquare(titleKey)
        #hashKeyQ = midSquare(quoteKey)

        # universal
        hashKeyT = universal(titleKey)
        hashKeyQ = universal(quoteKey)

        # multiplication
        #hashKeyT = multiplication(titleKey)
        #hashKeyQ = multiplication(quoteKey)

        # handle collisions
        t_collisions += handle_collisions(hashTitleTable, hashKeyT, movie.movie_name)
        q_collisions += handle_collisions(hashQuoteTable, hashKeyQ, movie.quote)
        
        counter += 1

end = time.time()
clock = end - start
# out of the loop, find unused buckets


print(f"""Title Method: 
    Unused: {unused_buckets(hashTitleTable)}
    Total Collisions: {t_collisions} 
    Time taken: {(clock):.3f} seconds""")

print(f"""Quote Method: 
    Unused: {unused_buckets(hashQuoteTable)}
    Total Collisions: {q_collisions}
    Time taken: {(clock):.3f} seconds""")
