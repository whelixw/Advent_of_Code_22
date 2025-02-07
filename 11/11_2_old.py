#Note: We never need to know the actual value of the items, only some of their properties.
# If we for each item keep track of the tests seperately, we have no issue of exploding values.
# each test kan be represented as the first digit of a base n number, where n is the value of tests.
# this corresponds to the modulo of the value of the item with the value of the test.
# the operations that need to be supported are multiplication and addition as well a the power of 2.
# it is well known how addition and multiplication can be done in base n.
# the power of 2 can be done found by taking the modulo of the power of 2 of the first digit of the base n number.
# 9 mod 11 = 9
# 9^2 = 81
# 81 mod 11 = 4
# 17 mod 11 = 6
# 6^2 = 36
# 36 mod 11 = 3
#17^2 mod 11 = 3

import heapq
test_list = []
def item_transfer(item, Monkey):
    global obj_list
    #print("item", item, "Monkey", Monkey)
    #if item > 10**9:
        #print("Monkey", Monkey)
    obj_list[Monkey].item_list.append(item)

class Monkey:
    def __init__(self, item_list, operation, test, friends):
        self.item_list = item_list
        self.operation = operation
        self.test = test
        self.code = compile(self.operation, "<string>", "eval")
        self.friends = friends
        self.counter = 0


    def initiate_item_list(self, item_list, test_list):
        new_item_list = []
        self.item_list = item_list
        self.test_list = test_list
        print(self.test_list, self.item_list)
        for item in item_list:
            for test in test_list:
                new_item_list.append([item%test])
        self.item_list = new_item_list
    def run_function(self):
        global test_dict
        while len(self.item_list) > 0:
            self.item_of_bases = self.item_list.pop()
            self.counter += 1
            print(self.item_of_bases)
            for index, item in enumerate(self.item_of_bases):
                print(item, index)
                self.item = [item, self.test_list[index]]
                self.worry = eval(self.code, {"__builtins__": None}, {"old": self.item})
                self.worry = self.worry%test_dict[index]
                self.item_of_bases[index] = self.worry


            #self.worry = eval(self.code, {"__builtins__": None}, {"old": self.item})

            #self.worry = int(self.worry/3)
            if self.item[test_dict[self.test]] == 0:
                item_transfer(self.worry, self.friends[0])
            else:
                item_transfer(self.worry, self.friends[1])

#obj_list = [Monkey([1], "old*3", 4, [1,2]), Monkey([2], "old*5", 7, [2,0]), Monkey([3], "old*7", 9, [0,1])]

input_doc = open("11/input.txt").readlines()
'''Monkey 0:
  Starting items: 76, 88, 96, 97, 58, 61, 67
  Operation: new = old * 19
  Test: divisible by 3
    If true: throw to monkey 2
    If false: throw to monkey 3'''

obj_list = []
with open("11/input.txt") as f:
    counter = 0
    for line in f.readlines():
        if counter%7 == 1:
            #print(line[18::])
            starting_items = list(map(int, line[18::].split(", ")))
        if counter%7 == 2:
            operation = line[19:-1]
        if counter%7 == 3:
            test = int(line[21:-1])
        if counter%7 == 4:
            friend1 = int(line[29:-1])
        if counter%7 == 5:
            friend2 = int(line[30:-1])
        if counter%7 == 6:
            print(starting_items, operation, test, friend1, friend2)
            test_list.append(test)
            obj_list.append(Monkey(starting_items, operation, test, [friend1, friend2]))
        counter += 1
    obj_list.append(Monkey(starting_items, operation, test, [friend1, friend2]))
    for obj in obj_list:
        obj.initiate_item_list(starting_items, test_list)

#order the tests
test_list = sorted(test_list)

#convert test_list to a dict that maps the test to the index
test_dict = {}
for index, test in enumerate(test_list):
    test_dict[test] = index

for i in range(10000):
    print(i)
    for index in range(len(obj_list)):
        #print(index)
        obj_list[index].run_function()

handled_counter_list = []
for obj in obj_list:
    handled_counter_list.append(obj.counter)
    #print the highest two values
largest = heapq.nlargest(2, handled_counter_list)
print(largest)
#print the product of the two highest values
print(largest[0]*largest[1])