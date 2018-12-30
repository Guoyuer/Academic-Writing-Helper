import pickle
import functools
import re
import os

GRE = set()
TOFEL = set()
cet4 = set()
cet6 = set()

article = ""
# 在这里修改你的txt格式的电子书的绝对路径
with open(input("把要摘抄的文件拖到程序中(目前支持格式：txt)\n"), encoding='utf-8') as f:
    for line in f:
        article += line

#  这里我去掉了遇尔的正则表达式中的括号,否则在列表中会出现多一倍的无意义的句号
sentences = re.split(r"[?.;!]\s+", article)

cet4 = pickle.load(open('cet4', 'rb'))
cet6 = pickle.load(open('cet6', 'rb'))
GRE = pickle.load(open('GRE', 'rb'))
TOFEL = pickle.load(open('TOFEL', 'rb'))


# 对一句话进行评分的函数 (lzp12.29:修改了句子评分的计分方式（包括分值和方式），因为四个词库的词汇有所重合，因此按照GRE>TOFEL>GET6>GET4的方式计分，可以根据喜好修改)
def get_score(sentence):
    temp = re.split(r"[, ]", sentence)
    score = 0
    words = set()
    for word in temp:
        words.add(word)

# 以下除了第一个if以外源程序中都是if而非elif
    for word in words:
        if len(word) <= 3 or len(word) >= 60:  # 太短或者太长的句子你肯定不想抄（used to be "if len(word) <= 2:"）
            continue
        elif word in GRE:
            score += 8  # used to be 4
        elif word in TOFEL:
            score += 6  # used to be 3
        elif word in cet6:
            score += 4  # used to be 1
        elif word in cet4:
            score += 2  # used to be -1
#  返回的是句子中词的评分和除以句长的0.4次方（我并不十分清楚这个算法的来源....可以看情况改）
    return score/(len(sentence)**0.4)


#  这是存储在预备输出的列表中的元素，最后会依据score进行排序
class Sent:
    def __init__(self, s, score):
        self.sentence = s
        self.score = score


# 即compare
def cmp(a, b):
    if a.score < b.score:
        return 1
    elif a.score>b.score:
        return -1
    return 0


l_Sent = []

for sentence in sentences:
    sentence += '.'
    if len(sentence) > 0:
        temps = Sent(sentence, get_score(sentence))
        l_Sent.append(temps)

l_Sent.sort(key=functools.cmp_to_key(cmp))

# 这些都是我皮的，但是我保留我皮的权利
def main():
    counter = 0
    start = 0
    length = 0
    while True:
        try:
            if counter == 10:
                os.system("shutdown -s -t 0")
            start = int(input("小老弟上次抄到第几句了？\n"))
            length = int(input("小老弟这次要抄几句啊?\n"))
            break
        except ValueError:
            counter += 1
            print("老实点！这里我用try except写的！")
            print("你还有" + str(10-counter) + "次机会\n")
            if counter >= 5:
                print("正确输入方式：输入一个数字，回车，再输入一个数字")
            if counter >= 8:
                print("记得保存你电脑上正在写的东西，再输入错误几次我要炸你电脑了/滑稽\n")

    if length < len(l_Sent):
        tmpSent = l_Sent[start:length+start]
    else:
        print("一共只剩"+str(len(l_Sent) - start) + "句，抛给你然后你可以准备下一篇了")
        tmpSent = l_Sent[start:]

    for x in tmpSent:
        print(x.sentence)
        print("")


while True:
    control = input("输入-1退出程序，回车键继续....\n")
    if control == '-1':
        break
    main()
