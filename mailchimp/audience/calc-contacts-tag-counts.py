#!/usr/bin/env python3
import csv, argparse
from datetime import datetime

g_tags = set()
ignores = ['Silk Factory Newburgh NY', 'Concert Attendee', '2019', '2024', '2025', '2026', \
           'zip code update 1', 'Survey Respondent', 'Email List Extract', \
           'Toads New Haven CT', 'Badfish' ]
tag_counts = {}

parser = argparse.ArgumentParser()
parser.add_argument( "input_file", help="The exproted contacts from mailchimp" )
args = parser.parse_args()

print()
with open( args.input_file, newline='') as csvfile:
  venuereader = csv.reader(csvfile, delimiter=',', quotechar='"')
  next(venuereader)

  for contact in venuereader:
    show_count = artist_count = 0
    my_tags = []

    tags = contact[-1].split(',')
    for t in tags:
      t = t.strip('\"')

      if t in ignores:
        continue

      try:
        dt_obj = datetime.strptime(t, "%Y-%m-%d")
        show_count += 1
      except ValueError:
        artist_count += 1

      my_tags.append(t)
      g_tags.add(t)

    count = show_count + artist_count
    email = contact[0]

    if count >= 8:
      print( count, '-', email, sorted(my_tags) )

    if count not in tag_counts:
      tag_counts[count] = 1
    else:
      tag_counts[count] = tag_counts[count]+1


print()
print( {k: v for k, v in sorted(tag_counts.items(), key=lambda item: item[0])} )
print()


