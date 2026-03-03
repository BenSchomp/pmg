#!/usr/bin/env python3
import sys, urllib.parse

if len(sys.argv) != 3:
  print( "! wrong numer of arguments !" )
  print()
  print( "required arguments: <agent_email_prefix> <artist_name>" )
  print( "example: $", sys.argv[0], 'jleo "A Farewell to Kings"' )
  print()
  exit(-1)

text = "mailto:{AGENT}@providencemusicgrp.com?subject=Booking+Interest&body="
body_text = "Hi, I would like to inquire about pricing and availability for: {ARTIST}\n\nThe best way to contact me is: \n\nThank You!"

(agent, artist) = (sys.argv[1], sys.argv[2])

text = text.replace( "{AGENT}", agent )
body_text = urllib.parse.quote_plus( body_text.replace( "{ARTIST}", artist ) )

result = text + body_text

print()
print( result )
print()


