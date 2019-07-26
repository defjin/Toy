import csv

def SortRank(sub_li): 
    sub_li.sort(key = lambda x: x[2]) 
    return sub_li 

with open('swProblem1.csv','w', encoding='utf-8',newline='') as f:
    with open('swProblem.csv', 'r', encoding='utf-8') as r:
        rdr = csv.reader(r)
        newlist = []
        for li in rdr:
            newlist.append(li)
        #rdr = [[번호,제목,난이도,C,C++,Java,Python] ...]
        
        #???SortRank(newlist)

        writer = csv.writer(f)
        for line in newlist :
            writer.writerow(line)