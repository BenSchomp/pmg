
file = open( 'venue types.txt', 'r' )

types = set()
for line in file:
  line = line.strip()
  parts = line.split(',')
  for p in parts:
    types.add(p.strip())

print( types )
for t in types:
  print( t )



