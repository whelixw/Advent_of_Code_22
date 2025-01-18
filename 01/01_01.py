import heapq

input_doc=open("01/input.txt")
list_of_sums = []
sum_of_lines = 0
current_line = input_doc.readline()
while current_line != "":
    #print(current_line)
    if current_line != "\n":
        sum_of_lines += int(current_line[:-1])
    else:
        list_of_sums.append(sum_of_lines)
        print(sum_of_lines)
        sum_of_lines = 0
    current_line = input_doc.readline()

print("max: "+str(max(list_of_sums)))
print("sum of 3 largest: "+str(sum(heapq.nlargest(3,list_of_sums))))