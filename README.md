# Subscription Tracker

A clean, modern personal finance dashboard designed to help you track recurring subscriptions, analyze monthly spending habits, and monitor upcoming renewals. Built with **Flask** and **Tailwind CSS**.

## 🚀 Features

- **Dashboard Overview**: Get a quick snapshot of your total monthly and annual costs.
- **Spending Analysis**: visual breakdown of spending by categories (Entertainment, Productivity, etc.).
- **Renewal Alerts**: Automatic calculation of next renewal dates with countdowns for upcoming payments in the next 90 days.
- **Flexible Billing Cycles**: Support for Monthly, Quarterly, and Annual billing cycles with automatic cost normalization.
- **Excel Export**: Download a detailed report of all your subscriptions for offline analysis.
- **Responsive Design**: Fully responsive UI that works seamlessly on desktop and mobile.

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite (Lightweight, serverless)
- **Frontend**: HTML5, Vanilla JavaScript
- **Styling**: Tailwind CSS via CLI
- **Data Export**: `openpyxl` for Excel generation

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/subscription-tracker.git
   cd subscription-tracker
   ```

2. **Set up the Python Environment**
   It's recommended to use a virtual environment.
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate it (Windows)
   venv\Scripts\activate

   # Activate it (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node dependencies (for Tailwind CSS)**
   ```bash
   npm install
   ```

## 🏃‍♂️ Usage

1. **Start the Tailwind Watcher** (Optional, only if modifying styles)
   ```bash
   npm run watch
   ```

2. **Run the Flask Application**
   ```bash
   python app.py
   ```

3. **Access the Dashboard**
   Open your browser and navigate to `http://localhost:5000`

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
