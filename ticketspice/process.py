import csv, re, argparse
from datetime import datetime

# Global dictionary to store ticket data
ticket_data = {}
VENUE_CITY_STATE = "Silk Factory Newburgh NY" # XXX
YEAR_OF_SHOW = DATE_OF_SHOW = ARTIST_NAME = PAGE_NAME = None

def import_data(file_path):
  global ticket_data
  global VENUE_CITY_STATE, YEAR_OF_SHOW, DATE_OF_SHOW, ARTIST_NAME, PAGE_NAME

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
          if not DATE_OF_SHOW:
            scan_date = row.get("First Scan Date")
            if scan_date:
              show_date = datetime.strptime(scan_date, "%Y-%m-%d %I:%M %p")
              YEAR_OF_SHOW = show_date.strftime("%Y")        # "2025"
              DATE_OF_SHOW = show_date.strftime("%Y-%m-%d")  # "2025-01-04"

  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
  except Exception as e:
    print(f"An error occurred: {e}")

def export_unique_emails(output_path):
  # Use a dictionary keyed by email to ensure uniqueness
  unique_customers = {}
  
  # Column mapping: "Source Column": "Target Column"
  mapping = {
    "Billing Email Address": "Email Address",
    "Billing Name (First Name)": "First Name",
    "Billing Name (Last Name)": "Last Name",
    "Billing Phone Number": "Phone Number",
    "Billing Address (Postal Code)": "Zip Code"
  }
  tags = ', '.join( ["Concert Attendee", VENUE_CITY_STATE, YEAR_OF_SHOW, DATE_OF_SHOW, ARTIST_NAME] )

  for ticket in ticket_data.values():
    email = ticket.get("Billing Email Address")
    if email and email not in unique_customers:
      unique_customers[email] = {mapping[k]: ticket.get(k, "") for k in mapping}
      unique_customers[email]['Tags'] = tags

  if not unique_customers:
    return

  fieldnames = list(mapping.values())
  fieldnames.append( "Tags" )
  with open(output_path, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for customer in unique_customers.values():
      writer.writerow(customer)

def print_ticket_summary():
  """
  Calculates and prints a summary of counts and subtotals grouped by price.
  """
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
  print("-" * 60)
  print(f"{'GRAND TOTAL':<33} | {grand_count:<10} | ${grand_amount:,.2f}")

if __name__ == "__main__":
  # Replace 'data.csv' with the actual path to your file
  input_file = 'data.csv' # TODO take from args
  output_file = 'unique_email_export.csv' # TODO create dynamic name

  # TODO receive tags from args?
  # usage: python3 process.py tickets.csv "Concert Attendee, Silk Factory Newburgh NY, Back in Black, 2026, 2026-02-27"

  # better usage: python3 process-tickets.csv
  # > Input file: "tickets (92).csv" (Y)? [most recent local .csv in listing]
  # > Tag users with: "Concert Attendee" (Y)? [default param]
  # > Tag users with: "Silk Factory Newburgh NY" (Y)? [default param]
  # > Tag users with: "2026" (Y)?
  # > Tag users with: "2026-02-28" (Y)? 2026-02-027 [yesterday's date]
  # > Tag users with: "Back in Black" (Y)? [Page Name up-to first , or -]
  
  import_data(input_file)
  
  if ticket_data:
    export_unique_emails(output_file)
    print_ticket_summary()
  else:
    print("No data imported. Please check the CSV file and column names.")
  print()
