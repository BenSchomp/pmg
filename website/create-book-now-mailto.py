import sys, urllib.parse

if len(sys.argv) != 3:
  print( "\nUSAGE: " + sys.argv[0] + " <agent_email_prefix> <double-quoted_artist_name>\n" )
  exit()

text = "mailto:{AGENT}@providencemusicgrp.com?subject=Booking+Interest&body="
body_text = "Hi, I would like to inquire about pricing and availability for: {ARTIST}\n\nThe best way to contact me is: \n\nThank You!"

(agent, artist) = (sys.argv[1], sys.argv[2])

text = text.replace( "{AGENT}", agent )
body_text = urllib.parse.quote_plus( body_text.replace( "{ARTIST}", artist ) )

result = text + body_text

print()
print( result )
print()


