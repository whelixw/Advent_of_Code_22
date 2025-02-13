with(open("13/input.txt")) as f:
    line_number = 0
    left_list = []
    right_list = []
    #lines are mod 3
    #first line contains a list. The list can be nested or empty and contains integers.
    #it should be read into a list
    #second contains the same data, but is read to a seperate list
    #third is skipped
    #repeat
    for line in f.readlines():
        if line_number%3 == 0:
            #print(line)
            left_list.append(eval(line))
            #print(list1)
        if line_number%3 == 1:
            right_list.append(eval(line))
            #print(list2)
        line_number += 1

def evalute_lists(left, right):
    i = 0
    while i < len(left) and i < len(right):
        if type(left[i]) == int and type(right[i]) == int:
            #if left is smaller then return
            if left[i] < right[i]:
                #print(left[i], right[i])
                return 0
            #if right is smaller then return 1
            elif left[i] > right[i]:
                #print(left[i], right[i])
                return 1
        elif type(left[i]) == list and type(right[i]) == list:
            #recursively call the function
            nested_return = evalute_lists(left[i], right[i])
            #if nested return is 1 then return 1
            if nested_return == 1:
                return 1
            #if nested return is 0 then return 0
            elif nested_return == 0:
                return 0
        #if one is a list and the other is an int, convert the int to a list
        elif type(left[i]) == int and type(right[i]) == list:
            left[i] = [left[i]]
            nested_return = evalute_lists(left[i], right[i])
            if nested_return == 1:
                return 1
            elif nested_return == 0:
                return 0
        elif type(left[i]) == list and type(right[i]) == int:
            right[i] = [right[i]]
            nested_return = evalute_lists(left[i], right[i])
            if nested_return == 1:
                return 1
            elif nested_return == 0:
                return 0
        i += 1
        #if right is longer then return 0
    if len(left) < len(right):
        return 0
    #if left is longer then return 1
    elif len(left) > len(right):
        return 1

i = 0
sum = 0
while i < len(left_list):
    left = left_list[i]
    right = right_list[i]
    print(left, right)
    if evalute_lists(left, right) == 0:
        print("true")
        sum += i+1
    else:
        print("false")
    i += 1
print(sum)


