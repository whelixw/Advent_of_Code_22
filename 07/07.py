##TODO cd ../

input_doc="""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""




input_doc=open("07/input.txt").readlines()
if type(input_doc)==str:
    input_doc = input_doc.split("\n")
dir_dict = {}
path_to_dir = []
read_flag = False
sublist = []
for line in input_doc:
    if line[-1] == "\n":
        line = line[:-1]
    print(path_to_dir)
    print(sublist)
    line = line.split(" ")

    if line[1] == "cd":
        if read_flag == True:
            read_flag = False
            dir_dict["".join(path_to_dir)] = sublist
            sublist = []
        if line[2] != "..":
            path_to_dir.append(line[2])
        else:
            path_to_dir.pop()

    elif line[1] == "ls":
        read_flag = True
    if read_flag == True:
        #space_split = line.split(" ")
        if line[0] == "dir":
            sublist.append(line[1])
        if line[0].isnumeric():
            sublist.append(line[0])
dir_dict["".join(path_to_dir)] = sublist

def find_small_dirs(key, lowsum = 0, totalsum = 0, threshold = 100000):
    for content in sorted(dir_dict[key], reverse=True):
        if not content.isnumeric():

            double_tuple = find_small_dirs(key+content)
            lowsum += double_tuple[0]
            totalsum += double_tuple[1]
            #print(totalsum)
        else:
            totalsum += int(content)
            #print(key)
            #print(totalsum)
    if totalsum <= threshold:
        lowsum += totalsum
    return (lowsum,totalsum)

output1=find_small_dirs("/")
print(output1[0])
space = 70000000 - output1[1]
threshold = 30000000-space

def find_small_dirs2(key, lowsum = 10**10, totalsum = 0, threshold = threshold):
    for content in sorted(dir_dict[key], reverse=True):
        if not content.isnumeric():

            double_tuple = find_small_dirs2(key+content, lowsum=lowsum)
            lowsum = min(double_tuple[0], lowsum)
            totalsum += double_tuple[1]
            #print(totalsum)
        else:
            totalsum += int(content)
            #print(key)
            #print(totalsum)
    #print(totalsum)
    #print(threshold)
    if totalsum >= threshold:
        #print(key)
        #print(totalsum)
        if totalsum < lowsum:
            print(totalsum)
            lowsum = totalsum
    return (lowsum,totalsum)

print(find_small_dirs2("/"))[0]