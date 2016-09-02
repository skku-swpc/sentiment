import codecs

w = codecs.open('matching_result.txt','w','utf-8')
with codecs.open('search_result.txt','r','utf-8') as file:
    while True:
        line = file.readline()
        if line == "end":
            break

        if 'matching' in line:
            if '.0' in line:
                w.write(line)

        else:
            continue
