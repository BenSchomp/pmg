import csv

contacts = []
for i in range(1000):
	filename = str(i) + ".out"
	#print( filename )

	#fields = [ 'Name', 'Email', 'Organization(s)', 'Preferred Phone', 'Website', 'Address', 'Industry', 'Status', 'Expiration Date' ]
	fields = [
		'Name', \
		'Email', \
		'Organization(s)', \
		'Role NULL', \
		'Related Artists NULL', \
		'Preferred Phone', \
		'Website', \
		'Address', \
		'City', \
		'State/Providence', \
		'Zip Code', \
		'Industry', \
		'Source', \
		'Status', \
		'Expiration Date', \
		]

	contact = {}
	key = 'Name'
	value = None

	with open(filename) as file:
	  for line in file:
	    line = line.strip()
	    if not line:
	      continue

	    parts = line.split('|')
	    for p in parts:
		    if p in fields:
		    	key = p
		    	value = None
		    else:
		    	if not value:
		    		value = p
		    	else:
			    	value = value + '|' + p
		    	contact[key] = value

	file.close()
	if len(contact):
		contact['Source'] = 'NC Fairs & Festivals 2025'
		if 'Address' in contact:
			parts = contact['Address'].split('|')
			address = ' | '.join( parts[:-1] )
			(city, state_zip) = parts[-1].split(',')
			(state, zipcode) = state_zip.strip().split(' ')
			assert( len(state) == 2 )

			contact['Address'] = address
			contact['City'] = city
			contact['State/Providence'] = state
			contact['Zip Code'] = zipcode

		contacts.append(contact)

#print( contacts )
#exit()

with open( "out.csv", 'w', newline='') as csvfile:
	writer = csv.DictWriter( csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL )
	writer.writeheader()
	writer.writerows(contacts)

csvfile.close()

