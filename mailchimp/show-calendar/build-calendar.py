import csv

# read csv file
rows = []
with open('calendar-data.csv', mode='r') as file:
  reader = csv.reader(file)
  for row in reader:
    rows.append( row )

light_mode = False
if light_mode:
  COLOR1 = "rgb(238, 175, 73)"
  COLOR2 = "rgb(71, 71, 71)"
else:
  COLOR1 = "rgb(240, 95, 38)"
  COLOR2 = "rgb(255, 255, 255)"

# output header html
print()
#print( '<h1 style="text-align: center;"><span style="color:'+COLOR1+';">UPCOMING SHOW CALENDAR</span></h1>' )
print( '<h4 style="text-align: left; direction: ltr;">' )
print( '  <span style="font-family: \'Source Sans 3\', \'Helvetica Neue\', Helvetica, Arial, sans-serif">' )

# output each row
for row in rows:
  (DATE, LINK, ARTIST, BILLING) = row
  print( '    <span style="font-size: 14px;color:'+COLOR2+'">'+DATE+' •&nbsp;</span>' )
  print( '    <a href="'+LINK+'" target="_blank" tabindex="-1" style="color:'+COLOR1+';"><strong><span style="font-size: 18px; color:'+COLOR1+';">'+ARTIST+'</span></strong></a>' )
  print( '    <span style="font-size: 14px; color:'+COLOR2+';"> •&nbsp;'+BILLING+'</span>' )
  print( '    <br/>' )

# output footer
print( '  </span>' )
print( '</h4>\n' )
