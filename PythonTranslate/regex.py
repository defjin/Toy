import re

hand = open('aa.txt')
for line in hand:
    line = line.rstrip()
    print(re.findall('^T[a-z0-9]+:', line))
    print(line)


x = 'My 2 favorite numbers are 19 and 42'
y = re.findall('fa(v.*?e)',x)
print(y)
