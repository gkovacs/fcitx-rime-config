dictionaries = '''
  - terra_pinyin_nospaces
  - terra_pinyin.extra_hanzi
  - luna_pinyin.sgmain
  - luna_pinyin.sgplus
  - luna_pinyin.sgplus2
  - luna_pinyin.chat
  - luna_pinyin.net
  - luna_pinyin.user
  - luna_pinyin.website
  - luna_pinyin.poetry
  - luna_pinyin.computer
  - luna_pinyin.place
  - luna_pinyin.shopping
'''

def get_words_in_dictionary(dictfile):
  lines = open(dictfile).readlines()
  output = []
  is_started = False
  for x in lines:
    x = x.strip()
    if x == '...':
      is_started = True
      continue
    if not is_started:
      continue
    if x == '':
      continue
    output.append(x)
  return output

def get_contents_in_dictionary(dictfile):
  lines = open(dictfile).readlines()
  output = []
  is_started = False
  for line in lines:
    x = line.strip()
    if x == '...':
      is_started = True
      continue
    if not is_started:
      continue
    output.append(line)
  return output

def get_pronunciations():
  output = {}
  lines = open('terra_pinyin_nospaces.dict.yaml').readlines()
  is_started = False
  for x in lines:
    x = x.strip()
    if x == '...':
      is_started = True
      continue
    if not is_started:
      continue
    if x == '':
      continue
    if '\t' not in x:
      continue
    parts = x.split('\t')
    char = parts[0]
    pronunciation = parts[1]
    char = char.strip()
    pronunciation = pronunciation.strip()
    if len(char) > 1:
      continue
    output[char] = pronunciation
  return output

for x in open('terra_pinyin_nospaces.dict.yaml'):
  print(x, end='')


for x in get_contents_in_dictionary('terra_pinyin.extra_hanzi.dict.yaml'):
  print(x, end='')

pronunciations = get_pronunciations()
dictionaries = dictionaries.split('-')
dictionaries = [x.strip() for x in dictionaries]
dictionaries = [x for x in dictionaries if x != '']
for dictionary_name in dictionaries:
  if dictionary_name.startswith('terra_pinyin'):
    continue
  dictfile = dictionary_name + '.dict.yaml'
  words = get_words_in_dictionary(dictfile)
  for word in words:
    skipword = False
    pronunciation = []
    for char in word:
      if char in pronunciations:
        pronunciation.append(pronunciations[char])
      else:
        skipword = True
        break
    if not skipword:
      print(word + '\t' + ''.join(pronunciation))