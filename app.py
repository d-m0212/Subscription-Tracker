from flask import Flask, render_template, request, jsonify, send_file
from database import init_db, get_all_subscriptions, add_subscription, delete_subscription, get_metrics, get_upcoming_renewals
from export_excel import generate_excel_report
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

app = Flask(__name__)

# Initialize database on startup
init_db()

def calculate_renewal_date(start_date_str, billing_cycle):
    """Calculate next renewal date based on start date and billing cycle"""
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    today = datetime.now()
    
    # Calculate the interval based on billing cycle
    if billing_cycle == 'monthly':
        delta = relativedelta(months=1)
    elif billing_cycle == 'quarterly':
        delta = relativedelta(months=3)
    elif billing_cycle == 'annual':
        delta = relativedelta(years=1)
    else:
        delta = relativedelta(months=1)  # default to monthly
    
    # Find the next renewal date from today
    renewal_date = start_date
    while renewal_date <= today:
        renewal_date += delta
    
    return renewal_date.strftime('%Y-%m-%d')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    subs = get_all_subscriptions()
    return jsonify(subs)

@app.route('/api/subscriptions', methods=['POST'])
def create_subscription():
    data = request.json
    
    # Validate required fields
    if not data.get('name') or not data.get('amount') or not data.get('start_date'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if float(data.get('amount', 0)) <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400
    
    # Handle custom category
    category = data.get('category')
    if category == 'Other' and data.get('customCategory'):
        category = data.get('customCategory')
    
    # Calculate renewal date
    billing_cycle = data.get('billing_cycle', 'monthly')
    renewal_date = calculate_renewal_date(data['start_date'], billing_cycle)
    
    sub_id = add_subscription(
        name=data['name'],
        amount=float(data['amount']),
        billing_cycle=billing_cycle,
        category=category,
        start_date=data['start_date'],
        renewal_date=renewal_date
    )
    
    return jsonify({'id': sub_id, 'message': 'Subscription added successfully'})

@app.route('/api/subscriptions/<int:sub_id>', methods=['DELETE'])
def remove_subscription(sub_id):
    delete_subscription(sub_id)
    return jsonify({'message': 'Subscription deleted successfully'})

@app.route('/api/metrics', methods=['GET'])
def api_metrics():
    metrics = get_metrics()
    return jsonify(metrics)

@app.route('/api/renewals', methods=['GET'])
def api_renewals():
    renewals = get_upcoming_renewals()
    return jsonify(renewals)

@app.route('/api/export', methods=['GET'])
def export_excel():
    filename = generate_excel_report()
    return send_file(filename, as_attachment=True, download_name='subscription_insights.xlsx')

if __name__ == '__main__':
    app.run(debug=True, port=5000)