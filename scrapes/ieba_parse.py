import re

file = open( 'ieba_032625_list.orig.html', 'r' )

contacts = []
contact_count = 0

cur_out = ''
for line in file:
	line = line.strip()

	if line == "</tr>":
		contacts.append( cur_out )
		cur_out = ''
	else:
		x = re.search( "<td style='text-align: left'>&nbsp;(.*)&nbsp;</td>", line )
		if x:
			if cur_out:
				cur_out = cur_out + ',"' + x.group(1) + '"'
			else:
				cur_out = '"' + x.group(1) + '"'

file.close()

for c in contacts:
	print( c )
