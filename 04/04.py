input_doc=open("04/input.txt")
current_pairs = input_doc.readline()
count_full_contained_pairs = 0
count_partially_contained_pairs = 0
while current_pairs != "":
    outer_split = str.split(current_pairs[:-1], ",")
    inner_split = [str.split(outer_split[0],"-"),str.split(outer_split[1],"-")]
    ranges_pairs = [range(int(i[0]),int(i[1])+1) for i in inner_split]
    intersecting_tasks = set.intersection(set(ranges_pairs[0]),set(ranges_pairs[1]))
    if (intersecting_tasks == set(ranges_pairs[0]) or intersecting_tasks == set(ranges_pairs[1])):
        count_full_contained_pairs += 1
    if not set.isdisjoint(set(ranges_pairs[0]),set(ranges_pairs[1])):
        count_partially_contained_pairs +=1
    current_pairs = input_doc.readline()
print(count_full_contained_pairs)
print(count_partially_contained_pairs)