#ci -*- coding: utf8 -*-
import xlrd
from konlpy.utils import pprint
from konlpy.tag import Twitter
from konlpy.tag import Kkma
import json
import codecs

twitter = Twitter()
kkma = Kkma()

result_file = codecs.open('search_result.txt','w','utf-8')

dic_list = []
origin = []
dic_count = 0
valence_list = []
with xlrd.open_workbook('dic.xlsx') as workbook:
    
    sheet =  workbook.sheet_by_index(1)
    sheet.cell_value(0,0)
    sheet.nrows
    sheet.ncols
    for row in range(sheet.nrows):
        verb = sheet.cell_value(row,0)

        if verb == u''or verb == u'원형' or verb == u'ㄱ'or  verb == u'ㄴ' or verb == u'ㄷ' or verb == u'ㅁ' or verb == u'ㅂ' or verb == u'ㅅ' or verb == u'ㅇ' or verb == u'ㅈ' or verb == u'ㅊ' or verb == u'ㅋ' or verb == u'ㅌ' or verb == u'ㅍ' or verb == u'ㅎ' or verb == u'이모티콘' or  verb == u'숫자':
            continue
        #dic_list.append([])
        valence_list.append([])
        dic_count = dic_count+1
        origin.append(verb)
        
        pos = twitter.pos(verb,norm=True,stem=True)
        
        for i in range(len(pos)):
            pos[i] = "{" + " : ".join(pos[i]) +"}"
        pos = ",".join(pos)
        dic_list.append(pos.split(","))
        #dic_list[dic_count-1].append(pos.split(","))
        valence_list[dic_count-1].append(sheet.cell_value(row,5))

text_list = []
count = 0

with codecs.open('searchtweet.json','r','utf-8') as data_file:
    while True:
        
        
        data = data_file.readline()
        if data == " \n" or data == "\n":
            continue
        
        if not data:
            break
        #text_list.append([])
        count = count+1
        
        text = data.split('"retweeted_status"')
        text = text[0].split(', "is_quote_status"')
        text = text[0].split('"text": "')
        r_text = text[1][:-1]
        
        result_file.write("text : "+r_text+"\n")
        result_file.write("sentences : "+" ".join(kkma.sentences(r_text))+"\n")
        result_file.write("nouns : "+",".join(kkma.nouns(r_text))+"\n")
        
        pos = twitter.pos(r_text,norm=True,stem=True)
        for i in range(len(pos)):
            pos[i] = "{" + " : ".join(pos[i]) +"}"
        pos = ",".join(pos)
        result_file.write("pos : "+pos+"\n")
        text_list.append(pos.split(","))
        #text_list[count-1].append(pos.split(","))
        
        #result = []
        #result_word = []
        result_file.write("matching : ")
        for j in range(dic_count):
            if set(text_list[count-1]) & set(dic_list[j]) == set(dic_list[j]):
                #result_file.write(" ".join(dic_list[j]) + " : "+str(valence_list[j][0]) +" ")
                result_file.write(origin[j] + " : "+str(valence_list[j][0]) +" ")
        result_file.write("\n\n")

result_file.write("end")

