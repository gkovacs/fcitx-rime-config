lines = open('leimaau_jyutping.dict.yaml').readlines()
#lines = open('terra_pinyin.dict.yaml').readlines()
output = []
for x in lines:
  #x = x.strip()
  if '\t' not in x:
    output.append(x)
  else:
    tabidx = x.index('\t')
    first = x[:tabidx]
    rest = x[tabidx:]
    rest = rest.replace(' ', '')
    #rest = rest.replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '')
    output.append(first + rest)
for x in output:
  print(x, end='')