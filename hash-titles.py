import csv


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
size = 10000 
# Going to use collision for this, so new tables needed
hashTitleTable = [[] for _ in range(size)]
hashQuoteTable = [[] for _ in range(size)]
prime = 31

file = "MOCK_DATA.csv"
counter = 0

# 5 hash functions

def hashFunctionOrd(key):
    hashValue = 0
    for char in key:
        # using prime to create randomness
        hashValue = (hashValue * prime + ord(char))
    newKey = hashValue % size
    return newKey

'''
def hashFunctionFolding(key):
    num = 0
    for i in key:
        num += ord(i)
    
    sum_digits = 0
    digits = []

    while num > 0:
        digits.append(num % 10)
        num //= 10

    for item in digits:
        sum_digits += item

    folded_index = sum_digits % size
    return folded_index
'''

#def hashFunctionPlaceholder():
    #pass

#def hashFunctionPlaceholder():
    #pass

#def hashFunctionPlaceholder():
    #pass

def handle_collisions_chaining(table, key, movie):
    # collision happens when a bucket is not empty
    collision_happened = len(table[key]) > 0
    table[key].append(movie)
    
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

with open(file, 'r', newline='',  encoding="utf8") as csvfile:
    reader = csv.reader(csvfile)
    
    title_collisions = 0
    quote_collisions = 0 
    
    for row in reader:
        if counter == 0:
            counter += 1
            continue
        movie = DataItem(row)

        firstFunctionTitle = hashFunctionOrd(movie.movie_name)
        firstFunctionQuote = hashFunctionOrd(movie.quote)

        title_collisions += handle_collisions_chaining(hashTitleTable, firstFunctionTitle, movie)
        quote_collisions += handle_collisions_chaining(hashQuoteTable, firstFunctionQuote, movie)

        # feed the appropriate field into the hash function
        # to get a key
        
        # mod the key value by the hash table length

        # try to insert DataItem into hash table
        # handle any collisions
        counter += 1

print(f"Title Collisions: {title_collisions}")
print(f"Quote Collisions: {quote_collisions}")
print(f"Unused title buckets: {unused_buckets(hashTitleTable)}")
print(f"Unused title buckets: {unused_buckets(hashQuoteTable)}")
print(f"Total movies: {counter - 1}")