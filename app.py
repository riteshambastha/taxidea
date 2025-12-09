"""
TaxIdea - NJ Property Tax Appeal Lead Generation Platform
A web application for identifying and managing tax appeal opportunities
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Global data storage
leads_data = None

# NJ Municipalities - Add CSV files as they're generated
municipalities = {
    # Monmouth County
    '13-28': {'name': 'Marlboro', 'county': 'Monmouth', 'file': 'marlboro_goldilocks_leads.csv'},
    '13-32': {'name': 'Wall', 'county': 'Monmouth', 'file': 'wall_goldilocks_leads.csv'},
    '13-21': {'name': 'Middletown', 'county': 'Monmouth', 'file': 'middletown_goldilocks_leads.csv'},
    '13-17': {'name': 'Howell', 'county': 'Monmouth', 'file': 'howell_goldilocks_leads.csv'},
    '13-30': {'name': 'Ocean', 'county': 'Monmouth', 'file': 'ocean_goldilocks_leads.csv'},
    
    # Middlesex County
    '12-04': {'name': 'East Brunswick', 'county': 'Middlesex', 'file': 'east_brunswick_goldilocks_leads.csv'},
    '12-25': {'name': 'Woodbridge', 'county': 'Middlesex', 'file': 'woodbridge_goldilocks_leads.csv'},
    '12-05': {'name': 'Edison', 'county': 'Middlesex', 'file': 'edison_goldilocks_leads.csv'},
    '12-12': {'name': 'Monroe', 'county': 'Middlesex', 'file': 'monroe_goldilocks_leads.csv'},
    
    # Bergen County
    '02-60': {'name': 'Teaneck', 'county': 'Bergen', 'file': 'teaneck_goldilocks_leads.csv'},
    '02-17': {'name': 'Fair Lawn', 'county': 'Bergen', 'file': 'fair_lawn_goldilocks_leads.csv'},
    '02-33': {'name': 'Paramus', 'county': 'Bergen', 'file': 'paramus_goldilocks_leads.csv'},
    '02-23': {'name': 'Hackensack', 'county': 'Bergen', 'file': 'hackensack_goldilocks_leads.csv'},
    
    # Essex County
    '07-14': {'name': 'Newark', 'county': 'Essex', 'file': 'newark_goldilocks_leads.csv'},
    '07-22': {'name': 'West Orange', 'county': 'Essex', 'file': 'west_orange_goldilocks_leads.csv'},
    '07-02': {'name': 'Bloomfield', 'county': 'Essex', 'file': 'bloomfield_goldilocks_leads.csv'},
    '07-10': {'name': 'Livingston', 'county': 'Essex', 'file': 'livingston_goldilocks_leads.csv'},
    
    # Morris County
    '14-29': {'name': 'Parsippany-Troy Hills', 'county': 'Morris', 'file': 'parsippany_troy_hills_goldilocks_leads.csv'},
    '14-35': {'name': 'Randolph', 'county': 'Morris', 'file': 'randolph_goldilocks_leads.csv'},
    '14-36': {'name': 'Rockaway', 'county': 'Morris', 'file': 'rockaway_goldilocks_leads.csv'},
    '14-27': {'name': 'Morris', 'county': 'Morris', 'file': 'morris_goldilocks_leads.csv'},
    
    # Somerset County
    '18-08': {'name': 'Franklin', 'county': 'Somerset', 'file': 'franklin_goldilocks_leads.csv'},
    '18-06': {'name': 'Bridgewater', 'county': 'Somerset', 'file': 'bridgewater_goldilocks_leads.csv'},
    '18-10': {'name': 'Hillsborough', 'county': 'Somerset', 'file': 'hillsborough_goldilocks_leads.csv'},
    
    # Union County
    '20-04': {'name': 'Elizabeth', 'county': 'Union', 'file': 'elizabeth_goldilocks_leads.csv'},
    '20-19': {'name': 'Union', 'county': 'Union', 'file': 'union_goldilocks_leads.csv'},
    '20-09': {'name': 'Linden', 'county': 'Union', 'file': 'linden_goldilocks_leads.csv'},
    
    # Ocean County
    '15-03': {'name': 'Brick', 'county': 'Ocean', 'file': 'brick_goldilocks_leads.csv'},
    '15-05': {'name': 'Jackson', 'county': 'Ocean', 'file': 'jackson_goldilocks_leads.csv'},
    '15-12': {'name': 'Toms River', 'county': 'Ocean', 'file': 'toms_river_goldilocks_leads.csv'},
    
    # Passaic County
    '16-35': {'name': 'Wayne', 'county': 'Passaic', 'file': 'wayne_goldilocks_leads.csv'},
    '16-18': {'name': 'Clifton', 'county': 'Passaic', 'file': 'clifton_goldilocks_leads.csv'},
    '16-27': {'name': 'Paterson', 'county': 'Passaic', 'file': 'paterson_goldilocks_leads.csv'},
}

def load_leads_data():
    """Load all available leads data"""
    global leads_data
    leads_data = {}
    available_count = 0
    missing_count = 0
    
    for muni_code, info in municipalities.items():
        file_path = info['file']
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if len(df) > 0:
                    df['Municipality'] = info['name']
                    df['County'] = info['county']
                    df['MuniCode'] = muni_code
                    leads_data[muni_code] = df
                    available_count += 1
                    print(f"✓ Loaded {len(df)} leads from {info['name']}, {info['county']} County")
            except Exception as e:
                print(f"✗ Error loading {info['name']}: {e}")
                missing_count += 1
        else:
            missing_count += 1
    
    print(f"\n📊 Summary: {available_count} municipalities loaded, {missing_count} pending analysis")
    
    if missing_count > 0:
        print(f"ℹ️  To analyze more municipalities, edit tax_appeal_pipeline.py and run it for each town")
    
    return leads_data

def get_all_leads():
    """Combine all leads into a single DataFrame"""
    if not leads_data:
        load_leads_data()
    
    if leads_data:
        return pd.concat(leads_data.values(), ignore_index=True)
    return pd.DataFrame()

def format_currency(value):
    """Format number as currency"""
    try:
        return f"${float(value):,.0f}"
    except:
        return "$0"

def format_ratio(value):
    """Format ratio as multiplier"""
    try:
        return f"{float(value):.2f}x"
    except:
        return "N/A"

# Template filters
app.jinja_env.filters['currency'] = format_currency
app.jinja_env.filters['ratio'] = format_ratio

@app.route('/')
def index():
    """Landing page"""
    load_leads_data()
    
    # Calculate stats
    all_leads = get_all_leads()
    stats = {
        'total_leads': len(all_leads),
        'total_overpayment': all_leads['Implied_Overpayment'].sum() if len(all_leads) > 0 else 0,
        'total_annual_savings': all_leads['Annual_Tax_Savings'].sum() if len(all_leads) > 0 else 0,
        'avg_savings_per_property': all_leads['Annual_Tax_Savings'].mean() if len(all_leads) > 0 else 0,
        'municipalities': len(municipalities)
    }
    
    return render_template('index.html', stats=stats, municipalities=municipalities)

@app.route('/search')
def search():
    """Search and filter leads"""
    all_leads = get_all_leads()
    
    if len(all_leads) == 0:
        return render_template('search.html', leads=[], filters={}, stats={})
    
    # Get filter parameters
    min_savings = request.args.get('min_savings', type=float, default=0)
    max_price = request.args.get('max_price', type=float, default=999999999)
    min_price = request.args.get('min_price', type=float, default=0)
    min_ratio = request.args.get('min_ratio', type=float, default=1.15)
    max_ratio = request.args.get('max_ratio', type=float, default=2.5)
    municipality = request.args.get('municipality', default='all')
    sort_by = request.args.get('sort', default='Implied_Overpayment')
    
    # Apply filters
    filtered = all_leads.copy()
    
    if min_savings > 0:
        filtered = filtered[filtered['Annual_Tax_Savings'] >= min_savings]
    
    if max_price < 999999999:
        filtered = filtered[filtered['Sale_Price'] <= max_price]
    
    if min_price > 0:
        filtered = filtered[filtered['Sale_Price'] >= min_price]
    
    if min_ratio > 0:
        filtered = filtered[filtered['Ratio'] >= min_ratio]
    
    if max_ratio < 10:
        filtered = filtered[filtered['Ratio'] <= max_ratio]
    
    if municipality != 'all':
        filtered = filtered[filtered['MuniCode'] == municipality]
    
    # Sort
    if sort_by in filtered.columns:
        filtered = filtered.sort_values(sort_by, ascending=False)
    
    # Calculate filtered stats
    filter_stats = {
        'count': len(filtered),
        'total_savings': filtered['Annual_Tax_Savings'].sum(),
        'avg_savings': filtered['Annual_Tax_Savings'].mean(),
        'total_overpayment': filtered['Implied_Overpayment'].sum()
    }
    
    # Convert to list of dicts for template
    leads_list = filtered.to_dict('records')
    
    filters = {
        'min_savings': min_savings,
        'max_price': max_price,
        'min_price': min_price,
        'min_ratio': min_ratio,
        'max_ratio': max_ratio,
        'municipality': municipality,
        'sort_by': sort_by
    }
    
    return render_template('search.html', 
                         leads=leads_list, 
                         filters=filters, 
                         stats=filter_stats,
                         municipalities=municipalities)

@app.route('/property/<muni_code>/<block>/<lot>')
def property_detail(muni_code, block, lot):
    """Property detail page"""
    all_leads = get_all_leads()
    
    # Find the specific property
    # Block and Lot might be integers or strings in CSV, URL params are always strings
    # Convert both to strings and strip for comparison
    property_data = all_leads[
        (all_leads['MuniCode'] == muni_code) & 
        (all_leads['Block'].astype(str).str.strip() == str(block).strip()) & 
        (all_leads['Lot'].astype(str).str.strip() == str(lot).strip())
    ]
    
    if len(property_data) == 0:
        return f"Property not found: {muni_code}, Block {block}, Lot {lot}", 404
    
    prop = property_data.iloc[0].to_dict()
    
    # Add some computed fields
    prop['tax_rate_estimate'] = 0.022  # 2.2% for Marlboro
    prop['current_annual_tax'] = prop['Assessed_Value'] * prop['tax_rate_estimate']
    prop['fair_annual_tax'] = prop['Sale_Price'] * 1.15 * prop['tax_rate_estimate']
    prop['overpayment_percentage'] = ((prop['Assessed_Value'] / prop['Sale_Price']) - 1) * 100
    
    # Parse sale date (MMDDYY)
    try:
        sale_date_str = str(prop['Sale_Date'])
        if len(sale_date_str) == 6:
            mm, dd, yy = sale_date_str[0:2], sale_date_str[2:4], sale_date_str[4:6]
            yyyy = '20' + yy if int(yy) <= 30 else '19' + yy
            prop['sale_date_formatted'] = f"{mm}/{dd}/{yyyy}"
        else:
            prop['sale_date_formatted'] = 'N/A'
    except:
        prop['sale_date_formatted'] = 'N/A'
    
    return render_template('property_detail.html', property=prop)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    all_leads = get_all_leads()
    
    stats = {
        'total_properties': len(all_leads),
        'total_overpayment': float(all_leads['Implied_Overpayment'].sum()),
        'total_annual_savings': float(all_leads['Annual_Tax_Savings'].sum()),
        'average_ratio': float(all_leads['Ratio'].mean()),
        'municipalities': len(municipalities)
    }
    
    return jsonify(stats)

@app.route('/map')
def property_map():
    """Interactive map of all properties"""
    all_leads = get_all_leads()
    
    # Convert to list of dicts for JavaScript
    properties = all_leads.to_dict('records') if len(all_leads) > 0 else []
    
    return render_template('map.html', properties=properties, municipalities=municipalities)

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    all_leads = get_all_leads()
    
    if len(all_leads) == 0:
        return render_template('dashboard.html', data={})
    
    # Calculate various analytics
    data = {
        'total_leads': len(all_leads),
        'by_municipality': all_leads.groupby('Municipality').size().to_dict(),
        'ratio_distribution': {
            '1.15-1.25': len(all_leads[(all_leads['Ratio'] >= 1.15) & (all_leads['Ratio'] < 1.25)]),
            '1.25-1.50': len(all_leads[(all_leads['Ratio'] >= 1.25) & (all_leads['Ratio'] < 1.50)]),
            '1.50-2.00': len(all_leads[(all_leads['Ratio'] >= 1.50) & (all_leads['Ratio'] < 2.00)]),
            '2.00+': len(all_leads[all_leads['Ratio'] >= 2.00])
        },
        'price_ranges': {
            '$200K-$400K': len(all_leads[(all_leads['Sale_Price'] >= 200000) & (all_leads['Sale_Price'] < 400000)]),
            '$400K-$600K': len(all_leads[(all_leads['Sale_Price'] >= 400000) & (all_leads['Sale_Price'] < 600000)]),
            '$600K-$800K': len(all_leads[(all_leads['Sale_Price'] >= 600000) & (all_leads['Sale_Price'] < 800000)]),
            '$800K+': len(all_leads[all_leads['Sale_Price'] >= 800000])
        },
        'top_10': all_leads.nlargest(10, 'Implied_Overpayment').to_dict('records'),
        'total_opportunity': float(all_leads['Implied_Overpayment'].sum()),
        'avg_opportunity': float(all_leads['Implied_Overpayment'].mean())
    }
    
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    print("=" * 60)
    print("TaxIdea - Property Tax Appeal Platform")
    print("=" * 60)
    load_leads_data()
    print("\n🚀 Starting web server...")
    print("📱 Open your browser to: http://localhost:5001")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)

