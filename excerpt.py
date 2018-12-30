import pickle
import functools
import re

GRE=set()
TOFEL=set()
cet4=set()
cet6=set()



# with open(r"C:\Users\GYE-LAPTOP\Desktop\GRE词汇表.txt") as f:
#     for line in f:
#         if line.split():
#             GRE.add(line.strip())
#
# with open(r"C:\Users\GYE-LAPTOP\Desktop\六级词汇表.txt",encoding='utf-8') as f:
#     for line in f:
#         line=line.strip()
#         if 'a'<=line[len(line)-1]<='z':
#             cet6.add(line)
#
# with open(r"C:\Users\GYE-LAPTOP\Desktop\四级词汇表.txt") as f:
#     for line in f:
#         line=line.strip()
#         pos=line.find(" ")
#         if pos>0:
#             cet4.add(line[0:pos])
#
# with open(r"C:\Users\GYE-LAPTOP\Desktop\托福词汇表.txt",encoding='utf-8') as f:
#     for line in f:
#         pos=line.find(" ")
#         line=line[pos+1:].strip()
#         if not line.startswith("x ") and line:
#             TOFEL.add(line.split(" ")[0])
#
#
# pickle.dump(cet4,open('cet4', 'wb'))
# pickle.dump(cet6,open('cet6', 'wb'))
# pickle.dump(TOFEL,open('TOFEL', 'wb'))
# pickle.dump(GRE,open('GRE', 'wb'))
#

article=""
with open(r"C:\Users\GYE-LAPTOP\Desktop\sample1.txt",encoding='utf-8') as f:
    for line in f:
        article+=line

sentences=re.split(r"[?.!]",article)

cet4=pickle.load(open('cet4', 'rb'))
cet6=pickle.load(open('cet6', 'rb'))
GRE=pickle.load(open('GRE', 'rb'))
TOFEL=pickle.load(open('TOFEL', 'rb'))


# 对一句话进行评分的函数
def get_score(sentence):
    temp=re.split(r"[?.!,;! ]",sentence)
    score=0
    for word in temp:
        if len(word)<=2:
            continue
        if word in GRE:
            score+=4

        if word in TOFEL:
            score+=3

        if word in cet6:
            score+=1
        if word in cet4:
            score-=2

    return score

class Sent:
    def __init__(self,s,score):
        self.sentence=s
        self.score=score


def cmp(a, b):
    if a.score<b.score:
        return 1
    elif a.score>b.score:
        return -1
    return 0

l_Sent=[]

for sentence in sentences:
    if len(sentence)>0:
        temps=Sent(sentence,get_score(sentence))
        l_Sent.append(temps)

l_Sent.sort(key=functools.cmp_to_key(cmp))

l_Sent=l_Sent[0:10]

for x in l_Sent:
    print(x.sentence)
    print("")
