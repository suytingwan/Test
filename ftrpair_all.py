# -*- coding:utf-8 -*-
import json

def tagwords():
    f = open('../data/tag_word.txt')
    words = []
    
    line = f.readline()
    words = line.split(' ')
    f.close()
    return words

def builddict():
    f = open('../data/book_ltp.txt')
    bookdict = {}
    while True:
        line = f.readline()
        if not line:
            break
        
        if '<Title>' in line:
            tag = line[7:len(line)].split('<')[0]
            #print tag
            while True:
                subline = f.readline()
                if 'Content:' in subline:
                    para = subline[9:len(subline)]
                    bookdict[tag] = para
                    break

    f = open('../data/jiangyi_ltp.txt')
    jydict = {}
    while True:
        line = f.readline()
        if not line:
            break

        if '<Title>' in line:
            tag = line[7:len(line)].split('<')[0]
            while True:
                subline = f.readline()
                if 'Content:' in subline:
                    para = subline[9:len(subline)]
                    jydict[tag] = para
                    break

    f = open('../data/tiku_ltp.txt')
    tikudict = {}
    while True:
        line = f.readline()
        if not line:
            break
        if '<Title>' in line:
            tag = line[7:len(line)].split('<')[0]
            #print tag
            while True:
                subline = f.readline()
                if 'QandA:' in subline:
                    para = subline[7:len(subline)]
                    #print 'yes',para
                    tikudict[tag] = para
                    break
             
    return bookdict, jydict, tikudict
            
                        

def findbook(tag):
    f = open('../data/book_ltp.txt')

    para = ''
    findtag = 0
    while True:
        line = f.readline()
        if not line:
            break
        
        if '<Title>' in line:
            #print tag
            #print line
            tag_s = tag.encode('utf-8')
            if tag_s[1:len(tag_s)] in line:
                while True:
                    subline = f.readline()                    
                    if 'Content:' in subline:
                        para = subline[7:len(subline)]
                        findtag = 1
                        break
        if findtag == 1:
            break
    return para            

def findjy(tag):
    f = open('../data/jiangyi_ltp.txt')

    para = ''
    findtag = 0
    while True:
        line = f.readline()
        if not line:
            break
        
        if '<Title>' in line:
            #print tag
            #print line
            tag_s = tag.encode('utf-8')
            if tag_s[1:len(tag_s)] in line:
                while True:
                    subline = f.readline()                    
                    if 'Content:' in subline:
                        para = subline[9:len(subline)]
                        findtag = 1
                        break
        if findtag == 1:
            break
    return para

def findtiku(tag):
    f = open('../data/tiku_ltp.txt')

    para = ''
    findtag = 0
    while True:
        line = f.readline()
        if not line:
            break
        
        if '<Title>' in line:
            #print tag
            #print line
            tag_s = tag.encode('utf-8')
            if tag_s[1:len(tag_s)] in line:
                while True:
                    subline = f.readline()                    
                    if 'QandA:' in subline:
                        para = subline[8:len(subline)]
                        findtag = 1
                        break
        if findtag == 1:
            break
    return para

print 'building dict ...'
bookdict, jydict, tikudict = builddict()
print 'building dicy done ...'

tips = json.load(open('./ftr_06_10.json'))
f = open('./06_10_sort.txt','w')
tagw = tagwords()
print tagw

for key in tips.keys():
    #print key 
    temp_tip = tips[key]
    title = temp_tip['title']

    answer = []
    for i in range(len(title)):
        #print title[i]
        #print (tagw[0]).decode('utf-8')

        if '选项：'.decode('utf-8') in title[i]:
            #print 'yes...'
            answer.append(title[i])
        
        if '正确答案'.decode('utf-8') in title[i]:
            #print 'yes'
            rightanw = title[i][len('正确答案'.decode('utf-8'))+1:len(title[i])]

    rightpos = 0
    #print answer
    #print rightanw
    for k in range(len(answer)):
         if rightanw in answer[k]:
            rightpos = k
            break
    '''        
    if rightpos == 0:
        evidence = temp_tip["A"]

    if rightpos == 1:
        evidence = temp_tip["B"]

    if rightpos == 2:
        evidence = temp_tip["C"]

    if rightpos == 3:
        evidence = temp_tip["D"]

    if rightpos == 4:
        evidence = temp_tip["E"]
    '''

    wordsplit = temp_tip['wordsplit']

    statement = ''
    for i in range(len(wordsplit)):
        #print i,wordsplit[i]
        endtag = wordsplit[i].index("\n")
        wordsplit[i] = wordsplit[i][0:endtag]
    
    #statement = wordsplit[0][1:len(wordsplit[0])]+wordsplit[rightpos+1][1:len(wordsplit[rightpos+1])]
    statement = wordsplit[0][1:len(wordsplit[0])]
    #print statement

    f.write(key+'\n')
    print rightpos
    
    f.write(str(rightpos)+' '+statement.encode('utf-8')+'\n')
    
    for i in range(5):
        f.write(str(i)+' '+(wordsplit[i+1][1:len(wordsplit[i+1])]).encode('utf-8')+'\n')
    
    for i in range(5):
        choice = wordsplit[i+1][1:len(wordsplit[i+1])]
        if i == 0:
            evidence = temp_tip["A"]
        if i == 1:
            evidence = temp_tip["B"]
        if i == 2 :
            evidence = temp_tip["C"]
        if i == 3:
            evidence = temp_tip["D"]
        if i == 4:
            evidence = temp_tip["E"]

        #para = ''
        paras = []
        scores = []
        
        if len(evidence) > 0:                
            for index in range(len(evidence)):
                #if index > 20:
                #    pass
                #else:
                para = ''
                evidence_tag = evidence[index].split(',')

                #print evidence_tag[1]
                score = float(evidence_tag[2])
                
                tag = evidence_tag[1][1:len(evidence_tag[1])]
                
                if evidence_tag[0] == 'BOOK':
                    #para = findbook(evidence_tag[1])
                    #tag = evidence_tag[1][1:len(evidence_tag[1])]
                    if tag.encode('utf-8') not in bookdict.keys():
                        pass
                    else:
                        para = 'BOOK '
                        para += bookdict[tag.encode('utf-8')]
                if evidence_tag[0] == 'JIANGYI':
                    #tag = evidence_tag[1][1:len(evidence_tag[1])]
                    if tag.encode('utf-8') not in jydict.keys():
                        pass
                    else:
                        para = 'JY '
                        para += jydict[tag.encode('utf-8')]
                if evidence_tag[0] == 'TIKU':
                    # tag = evidence_tag[1][1:len(evidence_tag[1])]
                    #print tikudict['179702']
                    if tag.encode('utf-8') not in tikudict.keys():
                        pass
                    else:
                        para = 'TK '
                        para += tikudict[tag.encode('utf-8')]
 
                #if len(para) > 0:
                #    f.write(str(i)+' '+para)
                if len(para) > 0:
                    paras.append(para)
                    scores.append(score)                   
                #print para

            # sort in score order and write evidence
            evi_count = []
            score_ = sorted(scores,reverse=True)
            for j in range(min(len(score_),20)):
                ind = scores.index(score_[j])
                scores[ind] += 0.02
                f.write(str(i)+' '+paras[ind])
            #print score_
            
        else:
            print 'evidence is a empty set'
    #break
    f.write('\n')
    
f.close()
        
