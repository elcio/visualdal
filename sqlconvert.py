#!/usr/bin/env python
# encoding: utf-8

import sys
from xml.etree.ElementTree import XML

def fielddef(row):
  types={
    'bit':'boolean',
    'date':'date',
    'datetime':'datetime',
    'decimal':'decimal(8,2)',
    'int':'integer',
    'mediumtext':'text',
    'tinyint':'integer',
    'varchar':'string',
  }
  attrs={
    'name':row.get('name'),
    'type':"'%s'" % types[row.find('datatype').text.lower().split('(')[0]],
  }
  c=row.find('comment')
  if c is not None:
    newattrs=dict([
      i.split('="') for i in c.text.replace('",','|||')[:-1].split('|||')
    ])
    if 'type' in newattrs:
      newattrs['type']="'%s'" % newattrs['type']
    attrs.update(newattrs)
  relation=row.find('relation')
  if relation is not None:
    tablename=relation.get('table')
    columnname=relation.get('row')
    if not 'f' in attrs:
      attrs['f']='%%(%s)s' % columnname
    attrs['type']='db.%s' % (tablename)
    attrs['requires']="IS_IN_DB(db,'%s.%s','%s')" % (tablename,columnname,attrs['f'])
  return attrs

# name, type, requires, label
def convert(xml):
  xml=XML(xml)
  text=""
  for table in xml.findall('table'):
    text+="db.define_table('%s',\n" % table.get('name')
    for row in table.findall('row'):
      row=fielddef(row)
      if row['name']!='id':
        if row['type']=="'string'":
          rt="'%s'" % row['name']
        else:
          rt="'%s',%s" % (row['name'],row['type'])
        if 'requires' in row:
          rt+=',requires=%s' % row['requires']
        if 'label' in row:
          rt+=",label='%s'" % row['label']
        text+="    Field(%s),\n" % rt
    text+=")\n\n"
  return text

if __name__=='__main__':
  print convert(open(sys.argv[1]).read())

