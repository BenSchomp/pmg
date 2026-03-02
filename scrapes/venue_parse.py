file = open( 'venues-2025-03-12.csv', 'r' )
next(file)

venues = []
venue_count = 0
cur_line = ''
for line in file:
	line = line.strip()

	if line[0] == '"':
		if cur_line:
			venues.append(cur_line)
		cur_line = line
	else:
		cur_line = cur_line + ', ' + line

venues.append(cur_line)
file.close()

# -----

for v in venues:
	print( v )
	parts = v.split(',')
	for p in parts:
		print( '*', p )
	exit()
