#NOTE: hvis du scaler worry ned, kan du scale summen op tilsvarende.
# squaring sker kun, hvis tallet er mod 11 eller mod 17
# a prime squared is divisible by itself, its prime and 1. 11*11 = 121, 121%11 = 0, 121%1 = 0, 121%121 = 0
# this can be used to reduce the power of the number (at least if it is a prime factor)
# the modifier is scaled up when the power is reduced, so the sum is still correct
# the sum can then be scaled down in a similar manner. (I think???)



import heapq

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



    def run_function(self):
        while len(self.item_list) > 0:
            self.item = self.item_list.pop()
            self.counter += 1
            self.worry = eval(self.code, {"__builtins__": None}, {"old": self.item})
            #self.worry = int(self.worry/3)
            if self.worry % self.test == 0:
                if self.test == 11 or self.test == 17:
                    modifier = self.test
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
            # make each item to a list of the item and 1
            starting_items = [[item, 1] for item in starting_items]
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
            obj_list.append(Monkey(starting_items, operation, test, [friend1, friend2]))
        counter += 1
    obj_list.append(Monkey(starting_items, operation, test, [friend1, friend2]))

for i in range(10000):
    #print(i)
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