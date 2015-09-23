#! /home/hujiangtao/localbuild_other_tools/scmtools/usr/bin/python

import os 
import re

data_dir = 's0'
pv = 0
epv = 0
mixer_epv = 0
mixer_ads = 0  # adnum_after_fcrpreproc
ppim_quality_epv = 0
ppim_quality_ads = 0
asn = 0

FIELDS=['res', 'adinf']

def process_one_line(line):
    global epv
    global mixer_epv
    global mixer_ads
    global ppim_quality_epv
    global ppim_quality_ads

    fields = {}
    for s in line.split():
        kv = s.split('=', 1)
        if (len(kv) < 2): 
            continue
        if kv[0] == 'res':
            # res=(0,)
            fields['res'] = int(re.findall('\d+', kv[1])[0])
            if fields['res'] != 0:
                epv += 1
        if kv[0] == 'adinf':
            # adinf=(2,0|0,0|0,0|0,0|0|0,0|0|0,0|0|0,0|0|0)
            # print kv[1]
            fields['adinf_preproc'] = int(kv[1].split(',')[0][1:])
            fields['adinf_ppim_quality'] = int(kv[1].split(',')[1].split('|')[0])
            if fields['adinf_preproc'] != 0:
                mixer_epv += 1
                mixer_ads += fields['adinf_preproc']
            if fields['adinf_ppim_quality'] != 0:
                ppim_quality_epv += 1
                ppim_quality_ads += fields['adinf_ppim_quality']
            # print fields['adinf_preproc']
            # print fields['adinf_ppim_quality']
    # fields = dict(s.split('=', 1) for s in line.split())
    # print fields

def process_lines(lines):
    for line in lines:
        process_one_line(line)


for f in os.listdir(data_dir):
    fn = os.path.join(data_dir, f)
    print 'fn: ', fn
    with open(fn) as fh:
        lines = fh.readlines()
        pv += len(lines)
        process_lines(lines)

print "pv:", pv
print "epv:", epv
print "pvr:", epv * 1.0 / pv
print "mixer_epv:", mixer_epv
print "mixer_pvr:", mixer_epv * 1.0 / pv
print "avg mixer_ads:", mixer_ads * 1.0 / pv
print "ppim_quality_epv:", ppim_quality_epv
print "ppim_quality_pvr:", ppim_quality_epv * 1.0 / pv
print "avg ppim_quality_ads:", ppim_quality_ads * 1.0 / pv



