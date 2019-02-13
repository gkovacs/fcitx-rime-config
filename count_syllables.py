import sys

lines = open('leimaau_jyutping.dict.yaml').readlines()
started = False
count = 0

alphabet = 'abcdefghijklmnopqrstuvwxyz123456'
alphabet_all = alphabet + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def is_valid_jp(jp):
  for c in jp:
    if c not in alphabet:
      return False
  return True

def strip_tone(jp):
  output = []
  for c in jp:
    if c in '123456':
      continue
    output.append(c)
  return ''.join(output)

def contains_english(char):
  for c in char:
    if c in alphabet_all:
      return True
  return False

def ends_with_one_of(reading, l):
  for elem in l:
    if reading.endswith(elem):
      return True
  return False

def is_complex_coda(coda):
  return coda.endswith('p') or coda.endswith('t') or coda.endswith('k') or coda.endswith('ng')

readings_set = set()
for line in lines:
  line = line.strip()
  if line == '...':
    started = True
    continue
  if not started:
    continue
  if line == '':
    continue
  parts = line.split('\t')
  if len(parts) < 2:
    continue
  char = parts[0]
  if contains_english(char):
    continue
  jp_word = parts[1]
  #print(jp_word)
  count += 1
  for jp in jp_word.split(' '):
    if not is_valid_jp(jp):
      print(line)
      print('invalid jp')
      sys.exit()
    jp = strip_tone(jp)
    readings_set.add(jp)
readings_list = sorted(list(readings_set))
#readings_list_orig = readings_list
#print(readings_list)
#readings_list = [x for x in readings_list if not ends_with_one_of(x, ['p', 't', 'k', 'ng'])]
readings_list = [x.replace('eo', 'oe') for x in readings_list]
print(readings_list)
print(len(readings_list))
# for x in readings_list:
#   if x[len(x) - 1] not in '123456':
#     print(x)
codas_set = set()
coda_cooccurrences = set()
codas_set_complex = set()
for c in list('abcdefghijklmnopqrstuvwxyz') + ['aa', 'gw', 'kw', 'ng']:
  valid_readings = [x for x in readings_list if x.startswith(c)]
  if c == 'a':
    valid_readings = [x for x in valid_readings if not x.startswith('aa')]
  if c == 'g':
    valid_readings = [x for x in valid_readings if not x.startswith('gw')]
  if c == 'k':
    valid_readings = [x for x in valid_readings if not x.startswith('kw')]
  if c == 'n':
    valid_readings = [x for x in valid_readings if not x.startswith('ng')]
  if len(valid_readings) == 0:
    print('free initial! ' + c)
    continue
  valid_readings_complex = [x for x in valid_readings if is_complex_coda(x)]
  valid_readings_noncomplex = [x for x in valid_readings if not is_complex_coda(x)]
  codas_complex = [x[len(c):] for x in valid_readings_complex]
  codas = [x[len(c):] for x in valid_readings_noncomplex]
  for coda in codas:
    codas_set.add(coda)
  for coda in codas_complex:
    codas_set_complex.add(coda)
  for coda in codas:
    for coda2 in codas:
      coda_cooccurrences.add(coda + ' ' + coda2)
  print(c + ' ' + str(len(valid_readings_noncomplex)))
  print(' '.join(valid_readings_noncomplex))
  print(c + ' complex ' + str(len(valid_readings_complex)))
  print(' '.join(valid_readings_complex))
codas_list = sorted(list(codas_set))
print(' '.join(codas_list))
print(len(codas_list))
codas_list_complex = sorted(list(codas_set_complex))
print(' '.join(codas_list_complex))
print(len(codas_list_complex))

print(coda_cooccurrences)
print(len(coda_cooccurrences))
print('non-cooccurring codas')
for coda in codas_list:
  if coda in []:
    continue
  for coda2 in codas_list:
    if (coda + ' ' + coda2) not in coda_cooccurrences:
      print(coda + ' ' + coda2)

for final in ['p', 't', 'k', 'ng']:
  print('finals that precede ' + final)
  print([x for x in codas_list_complex if x.endswith(final)])

# unify initials:
# o/kw, a/w, aa/gw?

# free initials (initially):
# a u e i o q r v x y

# e = k (final)
# i = t (final)
# u = p (final)
# a = ng (final)

# q = kw (initial)
# y = gw (initial)
# r = ng (initial)
# o = null initial

# x = tone 4
# v = tone 5

# unify finals:
# aa aai aam aan aau ai am an au e ei en/on/n/oen i m/im in iu o oei oi ou u/yu ui/oe un yun


# a/yun aa aai aam aan aau ai am an au e en/on/n/oen i/ei in iu m/im o oei oi ou u/yu ui/oe un

# q iu
# w oe/ui
# r aa
# t oi
# y un
# u u/yu
# i i/ei
# o o
# p aang (extra)
# a a/yun
# s ung (extra)
# d ai
# f an
# g am
# h aam
# j aan
# k aai
# l ong (extra)
# z ou
# x au
# c aau
# v oei
# b in
# n en/on/n/oen
# m m/im

# the following need 2 strokes to be entered (ones followed by slash have a single-key shortcut)
# finals that precede p
# ru au iu u ['aap', 'ap', 'ip', 'p']
# finals that precede t
# ri ai ii wi oi i ui ui ['aat', 'at', 'it', 'oet', 'ot', 't', 'ut', 'yut']
# finals that precede k
# re ae ee ie e we oe ue ['aak', 'ak', 'ek', 'ik', 'k', 'oek', 'ok', 'uk']
# finals that precede ng
# ra/p aa ea ia/t a wa oa/l ua/s ['aang', 'ang', 'eng', 'ing', 'ng', 'oeng', 'ong', 'ung']


# nearly non-occurring codas
# i ei
# ui oe
# yu ui

# seemingly overlappiong but screwed up when you add t
# yu u
# yu a

# non-cooccurring codas

# oen m un

# oen m
# oen ui
# ui m
# ui oen

# on en
# on oen
# on n
# n oen
# n en
# n on
# oen en
# oen n
# oen on
# yun n
# yu u
# yu '
# 