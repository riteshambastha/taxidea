"""
Analyze Multiple NJ Municipalities for Tax Appeal Opportunities
Runs the Goldilocks analysis for multiple townships and generates CSV files
"""

import subprocess
import sys

# Popular NJ municipalities with their county/district codes
MUNICIPALITIES = [
    # Monmouth County
    {'county': '13', 'district': '28', 'name': 'Marlboro', 'county_name': 'Monmouth'},
    {'county': '13', 'district': '32', 'name': 'Wall', 'county_name': 'Monmouth'},
    {'county': '13', 'district': '21', 'name': 'Middletown', 'county_name': 'Monmouth'},
    {'county': '13', 'district': '17', 'name': 'Howell', 'county_name': 'Monmouth'},
    
    # Middlesex County  
    {'county': '12', 'district': '04', 'name': 'East Brunswick', 'county_name': 'Middlesex'},
    {'county': '12', 'district': '25', 'name': 'Woodbridge', 'county_name': 'Middlesex'},
    {'county': '12', 'district': '05', 'name': 'Edison', 'county_name': 'Middlesex'},
    
    # Bergen County
    {'county': '02', 'district': '60', 'name': 'Teaneck', 'county_name': 'Bergen'},
    {'county': '02', 'district': '17', 'name': 'Fair Lawn', 'county_name': 'Bergen'},
    {'county': '02', 'district': '33', 'name': 'Paramus', 'county_name': 'Bergen'},
    
    # Essex County
    {'county': '07', 'district': '14', 'name': 'Newark', 'county_name': 'Essex'},
    {'county': '07', 'district': '22', 'name': 'West Orange', 'county_name': 'Essex'},
    {'county': '07', 'district': '02', 'name': 'Bloomfield', 'county_name': 'Essex'},
    
    # Morris County
    {'county': '14', 'district': '29', 'name': 'Parsippany-Troy Hills', 'county_name': 'Morris'},
    {'county': '14', 'district': '35', 'name': 'Randolph', 'county_name': 'Morris'},
    
    # Somerset County
    {'county': '18', 'district': '08', 'name': 'Franklin', 'county_name': 'Somerset'},
    {'county': '18', 'district': '06', 'name': 'Bridgewater', 'county_name': 'Somerset'},
    
    # Union County
    {'county': '20', 'district': '04', 'name': 'Elizabeth', 'county_name': 'Union'},
    {'county': '20', 'district': '19', 'name': 'Union', 'county_name': 'Union'},
]

def update_pipeline_config(county, district, name, county_name):
    """Update the tax_appeal_pipeline.py configuration"""
    
    # Read the current file
    with open('tax_appeal_pipeline.py', 'r') as f:
        content = f.read()
    
    # Update TARGET_COUNTY and TARGET_DISTRICT
    content = content.replace(
        f"TARGET_COUNTY = '13'    # Monmouth County",
        f"TARGET_COUNTY = '{county}'    # {county_name} County"
    )
    content = content.replace(
        f"TARGET_DISTRICT = '28'  # Marlboro Township", 
        f"TARGET_DISTRICT = '{district}'  # {name} Township"
    )
    
    # Update file paths
    content = content.replace(
        "modiv_file = '/Users/riteshambastha/projects/taxidea/modiv-2025/Monmouth.txt'",
        f"modiv_file = '/Users/riteshambastha/projects/taxidea/modiv-2025/{county_name}.txt'"
    )
    
    # Update output file
    safe_name = name.lower().replace(' ', '_').replace('-', '_')
    content = content.replace(
        "output_file = 'marlboro_goldilocks_leads.csv'",
        f"output_file = '{safe_name}_goldilocks_leads.csv'"
    )
    
    # Update print statement
    content = content.replace(
        'print(f"Target: County {TARGET_COUNTY} (Monmouth), District {TARGET_DISTRICT} (Marlboro)")',
        f'print(f"Target: County {{TARGET_COUNTY}} ({county_name}), District {{TARGET_DISTRICT}} ({name})")'
    )
    
    # Write back
    with open('tax_appeal_pipeline.py', 'w') as f:
        f.write(content)

def run_analysis(muni):
    """Run analysis for a municipality"""
    county = muni['county']
    district = muni['district']
    name = muni['name']
    county_name = muni['county_name']
    
    print(f"\n{'='*70}")
    print(f"Analyzing: {name}, {county_name} County (County {county}, District {district})")
    print(f"{'='*70}\n")
    
    try:
        # Update configuration
        update_pipeline_config(county, district, name, county_name)
        
        # Run the pipeline
        result = subprocess.run(
            ['python3', 'tax_appeal_pipeline.py'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Print output
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Successfully analyzed {name}")
            return True
        else:
            print(f"❌ Failed to analyze {name}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout analyzing {name}")
        return False
    except Exception as e:
        print(f"❌ Error analyzing {name}: {e}")
        return False

def main():
    print("="*70)
    print("NJ MULTI-MUNICIPALITY TAX APPEAL ANALYSIS")
    print("="*70)
    print(f"\nAnalyzing {len(MUNICIPALITIES)} municipalities...")
    print("This may take 10-15 minutes...\n")
    
    results = []
    
    for i, muni in enumerate(MUNICIPALITIES, 1):
        print(f"\n[{i}/{len(MUNICIPALITIES)}] Processing {muni['name']}...")
        success = run_analysis(muni)
        results.append({
            'name': muni['name'],
            'county': muni['county_name'],
            'success': success
        })
    
    # Print summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n✅ Successful: {len(successful)}/{len(MUNICIPALITIES)}")
    for r in successful:
        print(f"   • {r['name']}, {r['county']} County")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(MUNICIPALITIES)}")
        for r in failed:
            print(f"   • {r['name']}, {r['county']} County")
    
    print("\n📁 Generated CSV files:")
    import glob
    csv_files = glob.glob('*_goldilocks_leads.csv')
    for f in sorted(csv_files):
        print(f"   • {f}")
    
    print("\n🔄 Next step: Update app.py with all municipalities")
    print("   Run: python3 update_app_municipalities.py")

if __name__ == '__main__':
    main()

