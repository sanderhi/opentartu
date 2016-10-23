#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, string
from pyvabamorf import analyze
from pprint import pprint

import urllib2, codecs

IGN_TYYP = ['J', 'Z', 'D', 'P'] # sidesõna, lausemärk, operaator, küsisõna
IGN_WORD = ["olema"]

def ins_or_add(analysis, words):
	word = analysis['lemma']
	tyyp = analysis['partofspeech']
	#word=word+"_"+tyyp
	if tyyp not in IGN_TYYP and word not in IGN_WORD:
		if word in words.keys():
			words[word] = words[word] + 1
		else:
			words[word] = 1

def dl_doc(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()

def strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_content(url):
	resp = dl_doc(url)
	content = strip_html(resp)
	return content

def get_freq(data):
	words={}

	for word in data.split():
		word = word.lower()
		word = filter(unicode.isalpha, unicode(word, "utf-8"))
		if len(word) < 3:
			continue;
		res = analyze(word)
		ins_or_add(res[0]['analysis'][0], words)

	return sorted(words.items(), key=lambda x:x[1], reverse=True)

if len(sys.argv) >= 2:
	with open(sys.argv[1]) as f:
		data_file = f.readlines()

output=sys.argv[1].split(".")[0]+"-tags.csv"
fw = codecs.open(output,'w','utf-8')

print output

for line1 in data_file:
	url = line1.split()[0].strip('"')
	#print url
	if len(url)>15:
		data = get_content(url)
		aaa = get_freq(data)[0:20]
		tags = []
		for zzz in aaa:
			tags.append(zzz[0])
		line = "\""+url+"\",\"" + " ".join(tags) + "\""
		print line
		fw.write(line + "\n")

fw.close()

#pprint(words)


