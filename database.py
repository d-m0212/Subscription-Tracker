import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'subscriptions.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and create tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create subscriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            billing_cycle TEXT NOT NULL,
            category TEXT NOT NULL,
            renewal_date TEXT NOT NULL,
            start_date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_subscriptions():
    """Get all subscriptions with calculated monthly cost"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            name,
            amount,
            billing_cycle,
            category,
            renewal_date,
            start_date,
            CASE 
                WHEN billing_cycle = 'annual' THEN amount / 12
                WHEN billing_cycle = 'quarterly' THEN amount / 3
                ELSE amount 
            END as monthly_cost
        FROM subscriptions
        ORDER BY name
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def add_subscription(name, amount, billing_cycle, category, start_date, renewal_date):
    """Add a new subscription"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO subscriptions (name, amount, billing_cycle, category, renewal_date, start_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, amount, billing_cycle, category, renewal_date, start_date))
    
    sub_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return sub_id

def delete_subscription(sub_id):
    """Delete a subscription by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subscriptions WHERE id = ?', (sub_id,))
    
    conn.commit()
    conn.close()

def get_metrics():
    """Calculate total monthly cost, annual cost, and category breakdown"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total monthly cost
    cursor.execute('''
        SELECT 
            SUM(CASE 
                WHEN billing_cycle = 'annual' THEN amount / 12
                WHEN billing_cycle = 'quarterly' THEN amount / 3
                ELSE amount 
            END) as total_monthly
        FROM subscriptions
    ''')
    total_monthly = cursor.fetchone()[0] or 0
    
    # Category breakdown
    cursor.execute('''
        SELECT 
            category,
            SUM(CASE 
                WHEN billing_cycle = 'annual' THEN amount / 12
                WHEN billing_cycle = 'quarterly' THEN amount / 3
                ELSE amount 
            END) as monthly_cost
        FROM subscriptions
        GROUP BY category
        ORDER BY monthly_cost DESC
    ''')
    
    categories = {}
    for row in cursor.fetchall():
        categories[row[0]] = round(row[1], 2)
    
    # Total subscriptions
    cursor.execute('SELECT COUNT(*) FROM subscriptions')
    total_subs = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_monthly': round(total_monthly, 2),
        'total_annual': round(total_monthly * 12, 2),
        'total_subscriptions': total_subs,
        'categories': categories
    }

def get_upcoming_renewals(days=90):
    """Get subscriptions renewing in the next N days"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            name,
            amount,
            billing_cycle,
            category,
            renewal_date,
            julianday(renewal_date) - julianday('now') as days_until
        FROM subscriptions
        WHERE julianday(renewal_date) - julianday('now') BETWEEN 0 AND ?
        ORDER BY renewal_date ASC
    ''', (days,))
    
    rows = cursor.fetchall()
    conn.close()
    
    renewals = []
    for row in rows:
        renewals.append({
            'id': row[0],
            'name': row[1],
            'amount': row[2],
            'billing_cycle': row[3],
            'category': row[4],
            'renewal_date': row[5],
            'days_until': int(row[6])
        })
    
    return renewals