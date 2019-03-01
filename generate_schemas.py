#!/usr/bin/env python3

import json

from ruamel.yaml import YAML
from ruamel.yaml.reader import Reader

yaml = YAML(typ='safe')

def strip_invalid(s):
  res = ''
  for x in s:
    if Reader.NON_PRINTABLE.match(x):
      # res += '\\x{:x}'.format(ord(x))
      continue
    res += x
  return res

def get_base_schema(schema_name):
  return yaml.load(strip_invalid(open(schema_name + '_base.yaml', 'rt').read()))

def generate_jyutping_display():
  out = clone_schema('td_pinyin_flypy_jyutping')
  del out['speller']
  del out['translator']
  out['schema']['name'] = '注音雙拼'
  out['schema']['schema_id'] = 'td_pinyin_flypy_jyutping_display'
  out['schema']['dependencies'].extend(['leimaau_jyutping_zhuyin_nospaces', 'td_pinyin_flypy_jyutping'])
  out['putonghua_to_jyutping_reverse_lookup']['dictionary'] = 'leimaau_jyutping_zhuyin_nospaces'
  out['recognizer']['patterns']["putonghua_to_jyutping_lookup"] = "^[a-z]+[a-z;/,.]*$"
  return out

def generate_zhuyin_display():
  out = clone_schema('double_jyutping')
  del out['speller']
  del out['translator']
  out['schema']['name'] = '粵雙拼'
  out['schema']['schema_id'] = 'double_jyutping_display'
  out['schema']['dependencies'].extend(['double_jyutping', 'td_pinyin_flypy_jyutping'])
  #out['jyutping_to_putonghua_reverse_lookup']['dictionary'] = 'leimaau_jyutping_zhuyin_nospaces'
  out['recognizer']['patterns']["jyutping_to_putonghua_lookup"] = "^[abcdefghijklmnoprstuvwxyz]+[a-z;/,.]*$" # removed q from initial
  return out

def clone_schema(schema_name):
  if schema_name == 'td_pinyin_flypy_jyutping_display':
    return generate_jyutping_display()
  if schema_name == 'double_jyutping_display':
    return generate_zhuyin_display()
  #if schema_name == 'double_jyutping_display':
  #  schema_name = 'double_jyutping'
  return get_base_schema(schema_name)

def generate_key_binder(basename, newname, switchname, isqwerty):
  binding_base = yaml.load('''
  - {accept: "Control+Shift+f", toggle: zh_simp, when: always}
  - {accept: "Control+Shift+F", toggle: zh_simp, when: always}
  - {accept: "Control+Shift+t", toggle: zh_tw, when: always}
  - {accept: "Control+Shift+T", toggle: zh_tw, when: always}
  ''')
  nb = []
  if basename == 'double_jyutping' or basename == 'double_jyutping_display':
    nb.append({'accept': 'q', 'send': 'q', 'when': 'composing'})
    nb.append({'accept': 'q', 'send': '&', 'when': 'always'})
  if isqwerty:
    nb.append({'accept': 'Control+Shift+space', 'select': 'colemak_' + newname, 'when': 'always'})
    nb.append({'accept': 'Control+space', 'select': 'qwerty_' + newname, 'when': 'always'})
    nb.append({'accept': 'F35', 'select': switchname, 'when': 'always'})
    nb.append({'accept': 'Alt+space', 'select': switchname, 'when': 'always'})
  else:
    nb.append({'accept': 'Control+Shift+space', 'select': 'qwerty_' + newname, 'when': 'always'})
    nb.append({'accept': 'Control+space', 'select': 'colemak_' + newname, 'when': 'always'})
    nb.append({'accept': 'F35', 'select': switchname + '_colemak', 'when': 'always'})
    nb.append({'accept': 'Alt+space', 'select': switchname + '_colemak', 'when': 'always'})
  return binding_base + nb

def generate_key_binder_qwertycolemak(basename, newname, switchname, isqwerty):
  binding_base = yaml.load('''
  - {accept: "Control+Shift+f", toggle: zh_simp, when: always}
  - {accept: "Control+Shift+F", toggle: zh_simp, when: always}
  - {accept: "Control+Shift+t", toggle: zh_tw, when: always}
  - {accept: "Control+Shift+T", toggle: zh_tw, when: always}
  ''')
  nb = []
  if isqwerty:
    nb.append({'accept': 'Control+Shift+space', 'select': 'colemak_' + newname, 'when': 'always'})
    nb.append({'accept': 'Control+space', 'select': newname, 'when': 'always'})
    nb.append({'accept': 'F35', 'select': switchname, 'when': 'always'})
    nb.append({'accept': 'Alt+space', 'select': switchname, 'when': 'always'})
  else:
    nb.append({'accept': 'Control+Shift+space', 'select': 'qwerty_' + newname, 'when': 'always'})
    nb.append({'accept': 'Control+space', 'select': newname + '_colemak', 'when': 'always'})
    nb.append({'accept': 'F35', 'select': switchname + '_colemak', 'when': 'always'})
    nb.append({'accept': 'Alt+space', 'select': switchname + '_colemak', 'when': 'always'})
  return binding_base + nb

def generate_schema(basename, newname, switchname, isqwerty):
  out = clone_schema(basename)
  if basename == 'qwerty' or basename == 'colemak':
    out['schema']['schema_id'] = basename + '_' + newname
    #out['schema']['name'] = basename + '_' + newname
  else:
    if isqwerty:
      out['schema']['schema_id'] = newname
      #out['schema']['name'] = newname
    else:
      out['schema']['schema_id'] = newname + '_colemak'
      #out['schema']['name'] = newname + '_' + newname
  if basename == 'qwerty' or basename == 'colemak':
    out['key_binder']['bindings'] = generate_key_binder_qwertycolemak(basename, newname, switchname, isqwerty)
  else:
    out['key_binder']['bindings'] = generate_key_binder(basename, newname, switchname, isqwerty)
  return out

def write_schema(basename, newname, switchname, isqwerty):
  if basename == 'qwerty':
    filename = 'qwerty_' + newname + '.schema.yaml'
  elif basename == 'colemak':
    filename = 'colemak_' + newname + '.schema.yaml'
  else:
    if isqwerty:
      filename = newname + '.schema.yaml'
    else:
      filename = newname + '_colemak.schema.yaml'
  out = generate_schema(basename, newname, switchname, isqwerty)
  outf = open(filename, 'wt')
  outf.write(json.dumps(out, ensure_ascii=False, indent=2))
  outf.close()

def write_schemas(basename1, basename2, name1, name2):
  pairs = [
    [basename1, name1, name2, True],
    [basename1, name1, name2, False],
    [basename2, name2, name1, True],
    [basename2, name2, name1, False],
    ['qwerty', name1, name2, True],
    ['qwerty', name2, name1, True],
    ['colemak', name1, name2, False],
    ['colemak', name2, name1, False],
  ]
  for [bn,nn,sn,iq] in pairs:
    write_schema(bn, nn, sn, iq)

write_schemas('td_pinyin_flypy_jyutping', 'double_jyutping', 'td_pinyin_flypy_jyutping', 'double_jyutping')
write_schemas('td_pinyin_flypy_jyutping_display', 'double_jyutping_display', 'td_pinyin_flypy_jyutping_display', 'double_jyutping_display')

