from bs4 import BeautifulSoup
import sys

if len(sys.argv) != 2:
  exit()
filename = sys.argv[1]

with open(filename) as fp:
  soup = BeautifulSoup(fp, 'html.parser')

print( soup.get_text("|", strip=True) )

