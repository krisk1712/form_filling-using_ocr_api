import re
with open('result.txt', 'r') as res:
    text = res.readlines()
# print text
lin_cnt = text.count("\n")
print lin_cnt
a = ''
num_lines = sum(1 for line in open('result.txt'))
print num_lines
if num_lines == 3:
    for k in range(0, num_lines):
        a = a + text[k]
    # a = text[0] + text[1] + text[2]
    b = a.decode('unicode_escape').encode('ascii', 'ignore')
    c = str(b).split("-")
    final = []
    for items in c:
        final.append(re.sub('       ', '', items))

    print final
    print len(final)
    final1 = []
    for items in final:
        final1.append(re.sub('\n','',items))
    print final1
