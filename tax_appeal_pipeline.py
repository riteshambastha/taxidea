"""
NJ Property Tax Appeal Lead Generator
Identifies properties with assessments higher than recent sale prices
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================================
# CONFIGURATION - Change these to target different areas
# ============================================================================
TARGET_COUNTY = '13'    # Middlesex County
TARGET_DISTRICT = '21'  # Wall Township

# ============================================================================
# FIELD SPECIFICATIONS (1-based positions, converted to 0-based slices)
# ============================================================================

# MOD IV (Assessment) File Layout (0-based positions)
MODIV_FIELDS = {
    'County': (0, 2),
    'District': (2, 4),
    'Block': (4, 13),      # 9 chars - includes block and may have qualifier embedded
    'Lot': (13, 22),       # 9 chars
    'Qual': (22, 27),      # 5 chars
    'Property_Class': (56, 57),  # Single digit - 2 for residential
    'Address': (60, 95),
    'Owner_Name': (200, 250),  # Approximate - will trim
    'Net_Taxable_Value': (438, 447),  # 9-digit numeric value - the actual assessment
}

# SR1A (Sales) File Layout (0-based positions)
SR1A_FIELDS = {
    'County': (0, 2),
    'District': (2, 4),
    'Block': (350, 359),    # Later in record - includes block and qualifier
    'Lot': (359, 368),      # Comes right after block
    'Qual': (368, 373),     # After lot
    'Sale_Date': (19, 25),  # MMDDYY format
    'Sale_Price': (10, 19),  # Early in the record
    'NU_Code': (53, 56),    # Non-Usable code: '000' = code 0 (valid sale)
}

# ============================================================================
# DATA PARSING FUNCTIONS
# ============================================================================

def parse_fixed_width(filepath, field_specs, encoding='cp1252'):
    """
    Parse a fixed-width text file using field specifications.
    
    Args:
        filepath: Path to the fixed-width file
        field_specs: Dictionary of {field_name: (start, end)} positions (0-based)
        encoding: File encoding (legacy mainframe files typically use cp1252 or latin1)
    
    Returns:
        pandas DataFrame
    """
    print(f"📂 Reading {filepath}...")
    
    # Read all lines from the file
    with open(filepath, 'r', encoding=encoding, errors='replace') as f:
        lines = f.readlines()
    
    print(f"   Found {len(lines):,} records")
    
    # Parse each field according to specifications
    data = {}
    for field_name, (start, end) in field_specs.items():
        data[field_name] = [line[start:end].strip() if len(line) > start else '' 
                           for line in lines]
    
    df = pd.DataFrame(data)
    print(f"   Parsed {len(df.columns)} fields")
    
    return df


def clean_modiv_data(df, county_code, district_code):
    """
    Clean and filter MOD IV (assessment) data.
    
    Filters:
    - Target county and district
    - Residential properties only (Class 2)
    """
    print(f"\n🏘️  Processing MOD IV Assessment Data...")
    print(f"   Initial records: {len(df):,}")
    
    # Filter by geography
    df = df[(df['County'] == county_code) & (df['District'] == district_code)].copy()
    print(f"   After geography filter (County {county_code}, District {district_code}): {len(df):,}")
    
    # Filter by property class (2 = Residential)
    df = df[df['Property_Class'] == '2'].copy()
    print(f"   After property class filter (Residential only): {len(df):,}")
    
    # Convert Net Taxable Value to numeric
    df['Assessed_Value'] = pd.to_numeric(df['Net_Taxable_Value'], errors='coerce')
    
    # Create composite key for joining
    df['Join_Key'] = df['Block'].str.strip() + '|' + df['Lot'].str.strip() + '|' + df['Qual'].str.strip()
    
    # Keep only necessary columns
    df = df[['Join_Key', 'Block', 'Lot', 'Qual', 'Address', 'Owner_Name', 'Assessed_Value']].copy()
    
    # Remove records with missing or zero assessments
    df = df[df['Assessed_Value'] > 0].copy()
    print(f"   After removing zero/null assessments: {len(df):,}")
    
    return df


def clean_sr1a_data(df, county_code, district_code):
    """
    Clean and filter SR1A (sales) data.
    
    Filters:
    - Target county and district
    - Valid sales only (NU Code = '0' or empty/null)
    - Price floor of $200,000 (valid single-family homes only)
    """
    print(f"\n💰 Processing SR1A Sales Data...")
    print(f"   Initial records: {len(df):,}")
    
    # Filter by geography
    df = df[(df['County'] == county_code) & (df['District'] == district_code)].copy()
    print(f"   After geography filter (County {county_code}, District {district_code}): {len(df):,}")
    
    # Filter by NU Code (Non-Usable Code)
    # STRICT: Keep ONLY code '000' (code 0) - true arm's-length transactions
    # Reject: '010' (foreclosure), '026' (related party), '007' (estate), '019', etc.
    
    # Strip whitespace from NU codes
    df['NU_Code'] = df['NU_Code'].str.strip()
    
    # Keep only '000' (NU code 0 = valid arm's-length sale)
    df = df[df['NU_Code'] == '000'].copy()
    print(f"   After strict NU Code filter (code 0 only): {len(df):,}")
    
    # Convert Sale Price to numeric
    df['Sale_Price'] = pd.to_numeric(df['Sale_Price'], errors='coerce')
    
    # Apply price floor: $200,000 minimum (valid single-family homes)
    df = df[df['Sale_Price'] >= 200000].copy()
    print(f"   After $200K price floor (valid homes only): {len(df):,}")
    
    # Parse sale date (MMDDYY format)
    def parse_sale_date(date_str):
        if len(date_str) == 6:
            try:
                # MMDDYY format
                mm, dd, yy = date_str[0:2], date_str[2:4], date_str[4:6]
                # Assume 20XX for years 00-30, 19XX for 31-99
                yyyy = '20' + yy if int(yy) <= 30 else '19' + yy
                return pd.to_datetime(f"{yyyy}-{mm}-{dd}", errors='coerce')
            except:
                return pd.NaT
        return pd.NaT
    
    df['Sale_Date_Parsed'] = df['Sale_Date'].apply(parse_sale_date)
    
    # Create composite key for joining
    df['Join_Key'] = df['Block'].str.strip() + '|' + df['Lot'].str.strip() + '|' + df['Qual'].str.strip()
    
    # Keep only necessary columns
    df = df[['Join_Key', 'Block', 'Lot', 'Qual', 'Sale_Price', 'Sale_Date', 'Sale_Date_Parsed']].copy()
    
    return df


def identify_appeal_candidates(assessments_df, sales_df):
    """
    Merge assessment and sales data, calculate ratios, and identify over-assessed properties.
    Applies "Goldilocks" filtering to remove data artifacts and focus on legitimate appeals.
    """
    print(f"\n🔗 Merging Assessment and Sales Data...")
    
    # Merge on Block, Lot, Qual
    merged = pd.merge(
        sales_df,
        assessments_df,
        on='Join_Key',
        how='inner',
        suffixes=('_sale', '_assess')
    )
    
    print(f"   Matched records: {len(merged):,}")
    
    if len(merged) == 0:
        print("   ⚠️  No matching records found. Check county/district codes.")
        return pd.DataFrame()
    
    # Calculate the Assessment-to-Sale ratio
    merged['Ratio'] = merged['Assessed_Value'] / merged['Sale_Price']
    
    # Apply "Goldilocks" Ratio Filter (1.15 to 2.5)
    # < 1.15: Not enough savings to justify appeal
    # > 2.5: Likely data error or teardown (too complex)
    print(f"   Before Goldilocks filter: {len(merged):,} matched records")
    goldilocks = merged[(merged['Ratio'] >= 1.15) & (merged['Ratio'] <= 2.5)].copy()
    print(f"   After Goldilocks filter (1.15 ≤ Ratio ≤ 2.5): {len(goldilocks):,}")
    
    if len(goldilocks) == 0:
        print("\n   ℹ️  No properties found in the Goldilocks range (1.15-2.5)")
        return pd.DataFrame()
    
    # Calculate Implied Over-Assessment
    # Safe buffer: Market value should be Sale_Price * 1.15 (Chapter 123 common level range)
    # Anything above that is over-assessment
    goldilocks['Implied_Overpayment'] = goldilocks['Assessed_Value'] - (goldilocks['Sale_Price'] * 1.15)
    
    # Calculate potential annual tax savings (2.2% effective rate for Marlboro)
    EFFECTIVE_TAX_RATE = 0.022
    goldilocks['Annual_Tax_Savings'] = goldilocks['Implied_Overpayment'] * EFFECTIVE_TAX_RATE
    
    print(f"\n🎯 FOUND {len(goldilocks):,} LEGITIMATE APPEAL CANDIDATES!")
    print(f"   Average Ratio: {goldilocks['Ratio'].mean():.2f}")
    print(f"   Median Ratio: {goldilocks['Ratio'].median():.2f}")
    print(f"   Range: {goldilocks['Ratio'].min():.2f} to {goldilocks['Ratio'].max():.2f}")
    
    # Sort by Implied Over-Assessment descending (biggest winners first)
    goldilocks = goldilocks.sort_values('Implied_Overpayment', ascending=False)
    
    # Clean up columns for output
    goldilocks['Block'] = goldilocks['Block_sale']
    goldilocks['Lot'] = goldilocks['Lot_sale']
    
    output_df = goldilocks[[
        'Block', 
        'Lot', 
        'Address', 
        'Sale_Price', 
        'Assessed_Value', 
        'Ratio',
        'Implied_Overpayment',
        'Annual_Tax_Savings',
        'Sale_Date',
        'Owner_Name'
    ]].copy()
    
    return output_df


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("NJ PROPERTY TAX APPEAL LEAD GENERATOR - GOLDILOCKS EDITION")
    print("=" * 80)
    print(f"Target: County {TARGET_COUNTY} (Monmouth), District {TARGET_DISTRICT} (Wall)")
    print(f"Filters: Price ≥ $200K, Ratio 1.15-2.5, NU Code 0 or null only")
    print("=" * 80)
    
    # File paths (adjust as needed)
    modiv_file = '/Users/riteshambastha/projects/taxidea/modiv-2025/Monmouth.txt'
    sr1a_file = '/Users/riteshambastha/projects/taxidea/Sales2025.txt'
    output_file = 'middletown_goldilocks_leads.csv'
    
    try:
        # Parse the files
        modiv_df = parse_fixed_width(modiv_file, MODIV_FIELDS, encoding='cp1252')
        sr1a_df = parse_fixed_width(sr1a_file, SR1A_FIELDS, encoding='cp1252')
        
        # Clean and filter
        assessments = clean_modiv_data(modiv_df, TARGET_COUNTY, TARGET_DISTRICT)
        sales = clean_sr1a_data(sr1a_df, TARGET_COUNTY, TARGET_DISTRICT)
        
        # Find appeal candidates
        leads = identify_appeal_candidates(assessments, sales)
        
        if len(leads) > 0:
            # Save to CSV
            leads.to_csv(output_file, index=False)
            print(f"\n💾 Results saved to: {output_file}")
            
            # Display top 20 in enhanced format
            print("\n" + "=" * 120)
            print("TOP 20 GOLDILOCKS APPEAL CANDIDATES (Sorted by Est. Over-Assessment)")
            print("=" * 120)
            print(f"{'Address':<40} | {'Sale Price':>12} | {'Assessed Val':>12} | {'Ratio':>6} | {'Est. Over-Assessment ($)':>25}")
            print("-" * 120)
            
            for idx, row in leads.head(20).iterrows():
                address = row['Address'][:38]  # Truncate long addresses
                print(f"{address:<40} | ${row['Sale_Price']:>11,} | ${row['Assessed_Value']:>11,} | {row['Ratio']:>5.2f}x | ${row['Implied_Overpayment']:>23,.0f}")
            
            print("-" * 120)
            print(f"\n✅ Analysis complete! {len(leads)} Goldilocks leads identified.")
            print(f"📊 Total implied over-assessment: ${leads['Implied_Overpayment'].sum():,.0f}")
            print(f"💰 Total potential annual tax savings: ${leads['Annual_Tax_Savings'].sum():,.0f}")
            print(f"📈 Average ratio: {leads['Ratio'].mean():.2f}x (range: {leads['Ratio'].min():.2f}x - {leads['Ratio'].max():.2f}x)")
            
        else:
            print("\n⚠️  No properties found in the Goldilocks range (1.15-2.5) with current filters.")
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: Could not find file - {e}")
        print("Please check the file paths and try again.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

