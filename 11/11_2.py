import heapq
list_of_tests = []
def item_transfer(item, Monkey):
    global obj_list
    #print("item", item, "Monkey", Monkey)
    obj_list[Monkey].item_list.append(item)

class Monkey:
    def __init__(self, item_list, operation, test, friends):
        self.item_list = item_list
        self.operation = operation
        self.test = test
        self.code = compile(self.operation, "<string>", "eval")
        self.friends = friends
        self.items_handled = 0



    def run_function(self):
        global product_of_tests
        while len(self.item_list) > 0:
            self.item = self.item_list.pop(0)
            self.items_handled += 1
            self.worry = eval(self.code, {"__builtins__": None}, {"old": self.item})
            #print(self.worry, "worry")
            self.worry = self.worry%product_of_tests
            self.check = self.worry%self.test
            #print(self.check, "worry2", self.test)
            if self.check % self.test == 0:
                #print("true")
                item_transfer(self.worry, self.friends[0])
            else:
                #print("false")
                item_transfer(self.worry, self.friends[1])



#obj_list = [Monkey([1], "old*3", 4, [1,2]), Monkey([2], "old*5", 7, [2,0]), Monkey([3], "old*7", 9, [0,1])]

#input_doc = open("11/input.txt").readlines()
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
            list_of_tests.append(test)
        if counter%7 == 4:
            friend1 = int(line[29:-1])
        if counter%7 == 5:
            friend2 = int(line[30:-1])
        if counter%7 == 6:
            print(starting_items, operation, test, friend1, friend2)
            obj_list.append(Monkey(starting_items, operation, test, [friend1, friend2]))
        counter += 1
    obj_list.append(Monkey(starting_items, operation, test, [friend1, friend2]))
product_of_tests = 1
for test in list_of_tests:
    product_of_tests *= test


for i in range(10000):
    #print(i)
    for index in range(len(obj_list)):
        #print(index)
        obj_list[index].run_function()
    if i in [1, 20, 1000]:
        print(i)
        list_items_handled = []
        for obj in obj_list:
            list_items_handled.append(obj.items_handled)
        print(list_items_handled)

handled_counter_list = []
for obj in obj_list:
    handled_counter_list.append(obj.items_handled)
    #print the highest two values
largest = heapq.nlargest(2, handled_counter_list)
print(largest)
#print the product of the two highest values
print(largest[0]*largest[1])