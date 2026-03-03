#!/usr/bin/env python3
import csv, re, argparse
from datetime import datetime
from pathlib import Path

# Global dictionary to store ticket data
ticket_data = {}
VENUE_CITY_STATE = "Silk Factory Newburgh NY" # XXX
SHOW_YEAR = SHOW_DATE = ARTIST_NAME = PAGE_NAME = None

def import_data(file_path):
  global ticket_data
  global VENUE_CITY_STATE, SHOW_YEAR, SHOW_DATE, ARTIST_NAME, PAGE_NAME

  try:
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        # Ticket ID is the dictionary key
        ticket_id = row.get("Ticket ID")
        if ticket_id:
          ticket_data[ticket_id] = row

          # extract tags to send to mailchimp
          if not PAGE_NAME:
            PAGE_NAME = row.get("Page Name")
            if PAGE_NAME and not ARTIST_NAME:
              parts = re.split(r'[-|,]', PAGE_NAME, maxsplit=1)
              ARTIST_NAME = parts[0].strip()
          if not SHOW_DATE:
            scan_date = row.get("First Scan Date")
            if scan_date:
              dt_obj = datetime.strptime(scan_date, "%Y-%m-%d %I:%M %p")
              SHOW_YEAR = dt_obj.strftime("%Y")        # "2025"
              SHOW_DATE = dt_obj.strftime("%Y-%m-%d")  # "2025-01-04"

  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
  except Exception as e:
    print(f"An error occurred: {e}")
  else:
    print( "+ imported:", file_path )

def export_unique_emails(output_file):
  # Use a dictionary keyed by email to ensure uniqueness
  unique_customers = {}
  customer_count = 0
  
  # Column mapping: "Source Column": "Target Column"
  mapping = {
    "Billing Email Address": "Email Address",
    "Billing Name (First Name)": "First Name",
    "Billing Name (Last Name)": "Last Name",
    "Billing Phone Number": "Phone Number",
    "Billing Address (Postal Code)": "Zip Code"
  }


  tags = ', '.join( ["Concert Attendee", VENUE_CITY_STATE, SHOW_YEAR, SHOW_DATE, ARTIST_NAME] )

  for ticket in ticket_data.values():
    email = ticket.get("Billing Email Address")
    if email and email not in unique_customers:
      unique_customers[email] = {mapping[k]: ticket.get(k, "") for k in mapping}
      unique_customers[email]['Tags'] = tags
      customer_count += 1

  if not unique_customers:
    return

  fieldnames = list(mapping.values())
  fieldnames.append( "Tags" )
  with open(output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for customer in unique_customers.values():
      writer.writerow(customer)

  print( "+ exported:", output_file )
  print( "   (" + str(customer_count) + " unique contacts)" )

def print_ticket_summary():
  """
  Calculates and prints a summary of counts and subtotals grouped by price.
  """
  print( '\n>>', ARTIST_NAME, '@', VENUE_CITY_STATE, "~", SHOW_DATE, '<<' )
  print()
  print(f"{'Source':<10} | {'Ticket Price':<20} | {'Count':<10} | {'Amount'}")

  # Dictionary to aggregate: { price: { 'count': int, 'subtotal': float } }
  grand_count = grand_amount = 0
  origins = ['standard', 'boxoffice']
  for origin in origins:
    summary = {}
    total_count = total_amount = 0

    for ticket in ticket_data.values():
      if ticket['Originating Source'] != origin:
        continue
      if ticket['Status'] != 'completed':
        continue

      price_raw = ticket.get("Ticket Price ($ Amount)", "0")
      
      # Clean the price string (remove $, commas, and whitespace)
      try:
        price_clean = price_raw.replace('$', '').replace(',', '').strip()
        price = float(price_clean)
      except ValueError:
        continue

      if price not in summary:
        summary[price] = {"count": 0, "subtotal": 0.0}
      
      summary[price]["count"] += 1
      summary[price]["subtotal"] += price

    # Print the results
    print("-" * 60)
    
    # Sort by price for a cleaner report
    for price in sorted(summary.keys()):
      count = summary[price]["count"]
      subtotal = summary[price]["subtotal"]
      print(f"{origin:<10} | ${price:<19.2f} | {count:<10} | ${subtotal:,.2f}")
      total_count += count
      total_amount += subtotal

    print("-" * 60)
    print(f"{'     '+origin+' subtotal:':<34}| {total_count:<10} | ${total_amount:,.2f}")
    print()

    grand_count += total_count
    grand_amount += total_amount

  print("-" * 60)
  print(f"{'GRAND TOTAL':<33} | {grand_count:<10} | ${grand_amount:,.2f}")
  print("-" * 60)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("input_file", help="The exported ticketspice csv file to be imported.")
  parser.add_argument("--out_file", help="The filename of the mailchimp contacts csv to be written.")
  parser.add_argument("--artist", help='The artist name (a TAG: "Back in Black")')
  parser.add_argument("--venue", help='The venue name, city, and state (a TAG: "Silk Factory Newburgh NY")')
  parser.add_argument("--date", help="The show date (a TAG: 2026-02-27)")

  args = parser.parse_args()
  if args.artist:
    ARTIST_NAME = args.artist
  if args.date:
    dt_obj = datetime.strptime(args.date, "%Y-%m-%d")
    SHOW_YEAR = dt_obj.strftime("%Y")        # "2025"
    SHOW_DATE = dt_obj.strftime("%Y-%m-%d")  # "2025-01-04"
  if args.venue:
    VENUE_CITY_STATE = args.venue

  import_data(args.input_file)
  
  if ticket_data:
    bad_tags = False
    if not VENUE_CITY_STATE:
      print( "+ missing: VENUE_CITY_STATE" )
      bad_tags = True
    if not ARTIST_NAME:
      print( "+ missing: ARTIST_NAME" )
      bad_tags = True
    if not SHOW_DATE:
      print( "+ missing: SHOW_DATE" )
      bad_tags = True
    if not SHOW_YEAR:
      print( "+ missing: SHOW_YEAR" )
      bad_tags = True

    if bad_tags:
      print( "!! export failure: check input file, or use args to supliment data" )

    else:
      output_file = None
      if args.out_file:
        output_file = args.out_file
      else:
        p = Path(args.input_file)
        output_file = str(p.parent)+'/'+ARTIST_NAME.replace(" ","")+'_'+VENUE_CITY_STATE.replace(" ","")+'_'+SHOW_DATE+"_Contacts.csv"

      export_unique_emails(output_file)

    print_ticket_summary()

  else:
    print("No data imported. Please check the CSV file and column names.")
  print()
