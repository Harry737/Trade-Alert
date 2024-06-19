from flask import Flask, jsonify
from jugaad_data.nse import NSELive
import requests

app = Flask(__name__)

# Step 1: Fetch data from the GitHub URL
def fetch_data_from_github():
    github_url = "https://raw.githubusercontent.com/Harry737/Trade-Alert/main/stocks.txt"
    response = requests.get(github_url)
    return response.text.splitlines()

# Step 2: Initialize NSELive instance
n = NSELive()

# Endpoint to check stock prices
@app.route('/check_prices', methods=['GET'])
def check_prices():
    lines = fetch_data_from_github()
    results = []

    # Process each line and check stock prices
    for line in lines:
        if '>' in line:
            key, _, value = line.partition('>')
        elif '<' in line:
            key, _, value = line.partition('<')
        else:
            continue
        print(line)
        # Fetch stock data from NSELive
        q = n.stock_quote(key.strip())
        
        # Extract current price
        current_price = q['priceInfo']['intraDayHighLow']['value']
        print(current_price)
        # Compare current price with the specified value
        threshold_value = float(value.strip())
        if '>' in line:
            if current_price >= threshold_value:
                results.append(f"{key} price has increased.")
        elif '<' in line:
            if current_price <= threshold_value:
                results.append(f"{key} price has decreased.")
    
    print(results)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")
