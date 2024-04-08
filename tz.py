
fh = open('tmp_list', 'r')
a_list = fh.readlines()
b_list = []
for i in a_list:
    j = float(i.strip('\n'))
    b_list.append(j)
fh.close()

b_list.sort(reverse=True)

x = 1

for i,value in enumerate(b_list):
    x = x * value

for i,value in enumerate(b_list):
    if(value<1):
        print(i)
        break

print(len(b_list))
print(x)
