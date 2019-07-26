def sortN(li): 
    li.sort(key = lambda x: x[0]) 
    li.sort(key = lambda x: x[1])
    return li 

for i in range(int(input())):
    n, m = map(int, input().split())
    point_list = []
    road_list = [] 
    
    for l in range(m):
        x,y = map(int,input().split())
        if x>y :
            x,y = y,x
        point_list.extend([x,y])
        road_list.append((x,y))
    temp_list = []
    sorted_road = sortN(road_list)
    for idx,road in enumerate(sorted_road):
        temp_road = road[::]
        
        for idx2,road2 in enumerate(sorted_road):
            if idx2 <= idx :
                continue
            if temp_road[1] == road2[0] :
                temp_road = (temp_road[0], road2[1])
        temp_list.append(temp_road)
        
    if len(temp_list) ==0 :
        print('#{0} {1}'.format(i+1,1))
    else :
        print('#{0} {1}'.format(i+1,max(map(lambda x: x[1]-x[0]+1, temp_list))))