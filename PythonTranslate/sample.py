astr = ' Bob BBC '
print(astr.lstrip())
print(astr.rstrip())
print(astr.strip())

print(astr.capitalize())
print(astr.replace('B','C',1))
print(astr.startswith('ob'))
print(astr.startswith(' Bob'))

friends = []
#list()
friends.append('Jo')
friends.append('Garry')
friends.append('Sally')
print(friends)
print(sorted(friends))
print(friends)
friends.sort()
print(friends)

dict = { 'aa' : 1, 'bb': 2}
# dict()
dict['age'] = 21
print(dict)
x = dict.get('ab', -1)
print(x)
print(dict.keys())
print(list(dict))
print(dict.values())
print(list(dict.values()))
print(list(dict.items()))
for (aaa,bbb) in dict.items():
 print(aaa,bbb)

print(dict.values())
for a in dict.values():
 print(a)
