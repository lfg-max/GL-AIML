# app.py
from flask import Flask, render_template, request, send_file
import json
from datetime import datetime
from weasyprint import HTML
import os

app = Flask(__name__)

# Load session data
def load_sessions():
    try:
        with open('sessions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty list if file doesn't exist
        return []

# Save session data
def save_sessions(sessions):
    with open('sessions.json', 'w') as f:
        json.dump(sessions, f, indent=2)

# Get next invoice number for the month
def get_next_invoice_number(month_year):
    try:
        with open('invoice_counter.json', 'r') as f:
            counters = json.load(f)
    except FileNotFoundError:
        counters = {}
    
    current_count = counters.get(month_year, 0) + 1
    counters[month_year] = current_count
    
    with open('invoice_counter.json', 'w') as f:
        json.dump(counters, f, indent=2)
    
    return f"{current_count:03d}"

# Convert number to words (Indian numbering system)
def number_to_words(num):
    # Implementation similar to the JavaScript version
    # ... (full implementation would go here)
    # For brevity, I'll include a simplified version
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
             "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    if num == 0:
        return "Zero"
    
    def convert_less_than_thousand(n):
        if n == 0:
            return ""
        elif n < 10:
            return units[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + (" " + units[n % 10] if n % 10 != 0 else "")
        else:
            return units[n // 100] + " Hundred" + (" " + convert_less_than_thousand(n % 100) if n % 100 != 0 else "")
    
    result = ""
    if num >= 10000000:
        result += convert_less_than_thousand(num // 10000000) + " Crore "
        num %= 10000000
    if num >= 100000:
        result += convert_less_than_thousand(num // 100000) + " Lakh "
        num %= 100000
    if num >= 1000:
        result += convert_less_than_thousand(num // 1000) + " Thousand "
        num %= 1000
    if num > 0:
        result += convert_less_than_thousand(num)
    
    return result.strip() + " Rupees Only"

@app.route('/')
def calendar():
    sessions = load_sessions()
    
    # Group sessions by date for the calendar view
    sessions_by_date = {}
    for session in sessions:
        date_str = session['date']
        if date_str not in sessions_by_date:
            sessions_by_date[date_str] = []
        sessions_by_date[date_str].append(session)
    
    # Get current month and year for the calendar
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    return render_template('calendar.html', 
                         sessions_by_date=sessions_by_date,
                         current_month=current_month,
                         current_year=current_year)

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    session_date = request.form.get('date')
    session_topic = request.form.get('topic')
    session_amount = float(request.form.get('amount', 0))
    
    # Get current date for invoice
    invoice_date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate invoice number
    month_year = datetime.now().strftime('%m/%Y')
    invoice_number = get_next_invoice_number(month_year)
    full_invoice_number = f"{invoice_number}/{datetime.now().strftime('%m/%Y')}"
    
    # Calculate GST
    gst_rate = 0.18
    igst_amount = session_amount * gst_rate
    total_amount = session_amount + igst_amount
    
    # Convert amounts to words
    amount_in_words = number_to_words(int(round(total_amount)))
    tax_in_words = number_to_words(int(round(igst_amount)))
    
    # Render invoice template
    html = render_template('invoice_template.html',
                         invoice_date=invoice_date,
                         invoice_number=full_invoice_number,
                         session_topic=session_topic,
                         base_amount=session_amount,
                         igst_amount=igst_amount,
                         total_amount=total_amount,
                         amount_in_words=amount_in_words,
                         tax_in_words=tax_in_words)
    
    # Generate PDF
    pdf = HTML(string=html).write_pdf()
    
    # Save PDF temporarily
    filename = f"Invoice_{full_invoice_number.replace('/', '_')}.pdf"
    with open(filename, 'wb') as f:
        f.write(pdf)
    
    # Send file to user
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)