types = ['assistant',
'callback',
'car',
'company_main',
'fax',
'home',
'home_fax',
'isdn',
'main',
'mobile',
'other',
'other_fax',
'pager',
'radio',
'telex',
'tty_tdd',
'work',
'work_fax',
'work_mobile',
'work_pager']

for type in types:
	print '  Tel.%s{locals: [us_en: {tNam: %sdesc: }]}' % ((type+':').ljust(33), (type+',').ljust(29))