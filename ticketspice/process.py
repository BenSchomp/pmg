import csv

# Global dictionary to store ticket data
ticket_data = {}

def import_data(file_path):
  """
  Imports CSV data into the global ticket_data dictionary keyed by Ticket ID.
  """
  global ticket_data
  try:
    with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        # Use "Ticket ID" as the dictionary key
        ticket_id = row.get("Ticket ID")
        if ticket_id:
          ticket_data[ticket_id] = row
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

  for ticket in ticket_data.values():
    email = ticket.get("Billing Email Address")
    if email and email not in unique_customers:
      unique_customers[email] = {mapping[k]: ticket.get(k, "") for k in mapping}

  if not unique_customers:
    return

  fieldnames = list(mapping.values())
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
    print(f"{'SUBTOTAL':<34}| {total_count:<10} | ${total_amount:,.2f}")

    grand_count += total_count
    grand_amount += total_amount

  print("-" * 60)
  print("-" * 60)
  print(f"{'GRAND TOTAL':<33} | {grand_count:<10} | ${grand_amount:,.2f}")

if __name__ == "__main__":
  # Replace 'data.csv' with the actual path to your file
  input_file = 'data.csv'
  output_file = 'unique_email_export.csv'
  
  import_data(input_file)
  
  if ticket_data:
    export_unique_emails(output_file)
    print_ticket_summary()
  else:
    print("No data imported. Please check the CSV file and column names.")
  print()
