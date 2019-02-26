from make_zhuyin_jyutping_nospaces import *

def print_stroke_with_pronunciation(word, stroke, outfile=sys.stdout):
  zhu = get_zhuyin(word)
  jyut = get_jyutping(word)
  if zhu != None and jyut != None:
    #pronunciation = jyut
    pronunciation = stroke + '·' + zhu + jyut
  elif zhu != None and jyut == None:
    #return
    pronunciation = stroke + '·' + zhu
  elif jyut != None and zhu == None:
    pronunciation = stroke + '·' + jyut
  else:
    return
  print(word + '\t' + ''.join(pronunciation), file=outfile)

def main():
  #for x in get_header_in_dictionary('terra_pinyin.dict.yaml'):
  #  print(x, end='')
  outfile = open('stroke_zhuyin_jyutping.dict.yaml', 'wt')
  print_header('stroke_zhuyin_jyutping', outfile=outfile)
  for word,stroke in get_word_and_pinyin_in_dictionary('stroke.dict.yaml'):
    print_stroke_with_pronunciation(word.strip(), stroke.strip(), outfile=outfile)
  outfile.close()

if __name__ == '__main__':
  main()