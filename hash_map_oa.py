# Name: Kodie Artmayer
# OSU Email: artmayek@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/2022
# Description: Implementation of an open addressing Hash map


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Method clears the contents of the hash map.
        It does not change the underlying hash capacity
        """
        for i in range(0, self.capacity):               # loop for length of Dynamic Array capacity
            self.buckets.set_at_index(i, None)          # set each bucket to None
        self.size = 0                                   # set the size to 0
        return

    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key
        if the key is not in the hash map returns none
        """
        # quadratic probing required
        hashed = self.hash_function(key)                # variable for the hash function integer
        index = hashed % self.capacity                  # index for the key
        place = self.buckets.get_at_index(index)        # variable for value at index
        j = 0                                           #variable to increase quad probe
        while place is not None:                        #while we dont hit an empty spot
            if place.key == key:                        #if the Hash entry key is the key
                if place.is_tombstone is True:          #if the tombstone marker is true
                    return None                         #it doesnt really exist
                return place.value                      #if it is false return the value
            else:
                j += 1                                  #else begin quad probe
                quad_probe = index + j ** 2             #variable for quad probe index
                if quad_probe > self.capacity - 1:      #if the index is greater than the capacity minus 1
                    quad_probe = (index + j ** 2) % self.capacity       #modulo divide by the capacity
                place = self.buckets.get_at_index(quad_probe)           #update place variable
                if place is None:                                       #if we hit an empty spot
                    return None                                         #its not in the table
                elif place.key == key:                                  #if the hash entry key is the key
                    if place.is_tombstone is True:                      #if tombstone flag is set
                        return None                                     #it doesnt really exist
                    return place.value                                  #else return the value
        return None

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key/value pair in the hash map.
        """
        entry = HashEntry(key, value)                       #variable to insert Hash Entry class
        if self.table_load() >= 0.5:                        #check the table load
            self.resize_table(self.capacity * 2)            #resize if needed
        hashed = self.hash_function(key)                    #variable for the hash function integer
        index = hashed % self.capacity                      #index for the key
        place = self.buckets.get_at_index(index)            #variable for index value
        if place is None or place.is_tombstone is True:     #if there is nothing there or tombstone marker is set
            self.buckets.set_at_index(index, entry)         #set the hash entry at the index
            self.size += 1                                  #increase the size
        elif place is not None:                             #if there is a value there already
            if key == place.key:                            #if the key equals the index key
                self.buckets.set_at_index(index, entry)     #update the value
            else:
                for j in range(1, self.capacity):           #loop for probing
                    quad_probe = index + j ** 2             #variable for quad probe index
                    if quad_probe > self.capacity - 1:      #if we go past the capacity in the index
                        quad_probe = (index + j ** 2) % self.capacity   #modulo divide by the capacity
                    new_place = self.buckets.get_at_index(quad_probe)   #update place for index of quad probe
                    if new_place is not None:                           #if there is a value there
                        if new_place.key == key:                        #if it equals the key
                            self.buckets.set_at_index(quad_probe, entry)    #update the value
                            return
                    if new_place is None or new_place.is_tombstone is True:     #if there is nothing there or tombstone is set
                        self.buckets.set_at_index(quad_probe, entry)            #enter the value pair
                        self.size += 1                                          #increase the size
                        return

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value
        from the hash map.
        """
        hashed = self.hash_function(key)                    # variable for the hash function integer
        index = hashed % self.capacity                      # variable for the index
        place = self.buckets.get_at_index(index)            # variable to access place in hash map
        if place is not None:                               #value at the index is not none
            if place.key == key:                            #if the keys match
                if place.is_tombstone is False:             #and the tombstone flag is not set
                    place.is_tombstone = True               #set the tombstone flag
                    self.size -= 1                          #decrease the size
                    return
        for j in range(0, self.capacity):                   # loop for quad probe
            quad_probe = index + j ** 2                     # variable for quad probe
            if quad_probe > self.capacity - 1:              # if the quad probe index is too large
                quad_probe = (index + j ** 2) % self.capacity  # modulo divide by the capacity
            new_place = self.buckets.get_at_index(quad_probe)  # new place location for quad probe index
            if new_place is not None:                           # if that location is not none
                if new_place.key == key:                        # if the keys match
                    if new_place.is_tombstone is False:         #if the tomstone flag is not set
                        new_place.is_tombstone = True           # flip tombstone to true
                        self.size -= 1                          #decrease the size
        return


    def contains_key(self, key: str) -> bool:
        """
        Method returns true if the key is in the hash map
        """
        # quadratic probing required
        hashed = self.hash_function(key)  # variable for the hash function integer
        index = hashed % self.capacity  # variable for the index
        place = self.buckets.get_at_index(index)  # variable to access index location
        if place is None:                           #if the value at the place is none
            return False                            #return false
        while place is not None:                    #loop to check hash map
            if place.key == key:                    #if the key at the place is the same as the key were looking for
                if place.is_tombstone is True:      #if tombstone flag is set
                    return False                    #its not really there
                return True                         #if its not set return true
            else:                                   #start the quad probe
                for j in range(1, self.capacity - 1):                           #loop for quad probe
                    quad_probe = index + j ** 2                                 #variable for quad probe index
                    if quad_probe > self.capacity - 1:                          #if the index is greater than the capacity
                        quad_probe = (index + j ** 2) % self.capacity           #modulo divide by the capacity
                    new_place = self.buckets.get_at_index(quad_probe)           #variable for quad probe index
                    if new_place is not None:                                   #if the index is not None
                        if new_place.key == key:                                #if the keys match
                            if new_place.is_tombstone is True:                  #if the tombstone flag is set
                                return False                                    #doesnt really exist
                            return True                                         #if its not return true
                    elif new_place is None:                                     #if we hit none we can stop looking
                        return False
        return False

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the
        hash table
        """
        counter = 0                                 # counter for the empty buckets
        for i in range(0, self.capacity):           # loop for the dynamic array
            place = self.buckets.get_at_index(i)         # variable to get length
            if place is None or place.is_tombstone is True:
                counter += 1                        # increase the counter for the empty buckets
        return counter                              # return the number of empty buckets

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor
        """
        return self.size/self.capacity              #current size divided by current capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table.
        """
        if new_capacity < 1:                                    #if the new capacity is less than 1
            return                                              #do nothing
        if new_capacity < self.size:                            #if the new capacity is less than the current size
            return                                              #do nothing
        new_buckets = DynamicArray()                            #new array to set up empty buckets
        new_array = DynamicArray()                              #new array to hold values in the hash map
        for i in range(0, new_capacity):                        #loop to create the new bucket array the correct size
            new_buckets.append(None)
        for i in range(0, self.capacity):                       #loop to get values in current buckets
            place = self.buckets.get_at_index(i)                #variable for index
            if place is not None:                               #if there is a value at the index
                if place.is_tombstone is False:                 #and the tombstone flag is not set
                    new_array.append(place)                     #append it to the array
        self.buckets = new_buckets                              #make the old buckets array the new buckets array
        self.capacity = new_capacity                            #update the capacity
        self.size = 0                                           #reset the size
        for i in range(0, new_array.length()):                  #loop for the new_array
            place = new_array.get_at_index(i)                   #variable for the index location
            self.put(place.key, place.value)                    #call put to rehash the values and enter them in the buckets
        return

    def get_keys(self) -> DynamicArray:
        """
        Method returns a Dynamic Array that contains
        all the keys in the hash map
        """
        return_array = DynamicArray()                       #new array to hold keys
        for i in range(0, self.capacity):                   #loop to look over hash map
            place = self.buckets.get_at_index(i)            #variable for index location
            if place is not None:                           #if the value is None
                if place.is_tombstone is False:             #and the tombstone flag is not set
                    return_array.append(place.key)          #append the key to the new array
        return return_array                                 #return array of keys


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
