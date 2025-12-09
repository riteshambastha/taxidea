#!/usr/bin/env python3
"""
Export leads for contact enrichment via skip tracing services.

This script exports your tax appeal leads in a format ready for
upload to skip tracing services like BatchSkipTracing.com.
"""

import pandas as pd
import glob
import os
from datetime import datetime

def export_for_enrichment():
    """Export all leads to enrichment-ready CSV"""
    
    print("=" * 70)
    print("📧 CONTACT ENRICHMENT EXPORT TOOL")
    print("=" * 70)
    print()
    
    # Find all goldilocks leads CSVs
    csv_files = glob.glob('*_goldilocks_leads.csv')
    
    if not csv_files:
        print("❌ No lead files found!")
        print("   Run tax_appeal_pipeline.py first to generate leads.")
        return
    
    print(f"📂 Found {len(csv_files)} lead files:")
    for f in csv_files:
        print(f"   • {f}")
    print()
    
    # Load all leads
    all_leads = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        
        # Extract municipality from filename
        muni_name = csv_file.replace('_goldilocks_leads.csv', '').title()
        df['Municipality'] = muni_name
        
        all_leads.append(df)
        print(f"   ✓ Loaded {len(df)} leads from {muni_name}")
    
    # Combine all
    combined = pd.concat(all_leads, ignore_index=True)
    print()
    print(f"📊 Total leads: {len(combined)}")
    print()
    
    # Prepare enrichment input
    # Most skip tracing services want: First Name, Last Name, Address, City, State, Zip
    enrichment_df = combined[['Address', 'Owner_Name', 'Municipality']].copy()
    
    # Add state (all NJ)
    enrichment_df['State'] = 'NJ'
    
    # Try to split owner name into first/last
    enrichment_df['Full_Name'] = enrichment_df['Owner_Name'].fillna('')
    
    # Split on comma (Last, First) or space (First Last)
    def split_name(full_name):
        if not full_name or pd.isna(full_name):
            return '', ''
        
        full_name = str(full_name).strip()
        
        # Format: "LAST, FIRST"
        if ',' in full_name:
            parts = full_name.split(',')
            return parts[1].strip() if len(parts) > 1 else '', parts[0].strip()
        
        # Format: "FIRST LAST" or "FIRST MIDDLE LAST"
        parts = full_name.split()
        if len(parts) >= 2:
            return parts[0], parts[-1]  # First name, Last name
        
        return full_name, ''  # Single word = last name
    
    enrichment_df[['First_Name', 'Last_Name']] = enrichment_df['Full_Name'].apply(
        lambda x: pd.Series(split_name(x))
    )
    
    # Also include property identifiers for matching back
    enrichment_df['Block'] = combined['Block']
    enrichment_df['Lot'] = combined['Lot']
    
    # Add value data (helpful for prioritization)
    enrichment_df['Annual_Tax_Savings'] = combined['Annual_Tax_Savings']
    enrichment_df['Ratio'] = combined['Ratio']
    
    # Final columns in order skip tracers expect
    output_columns = [
        'First_Name',
        'Last_Name',
        'Full_Name',
        'Address',
        'Municipality',
        'State',
        'Block',
        'Lot',
        'Annual_Tax_Savings',
        'Ratio'
    ]
    
    final_df = enrichment_df[output_columns].copy()
    
    # Remove rows with no address (can't enrich)
    final_df = final_df[final_df['Address'].notna() & (final_df['Address'] != '')]
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'leads_for_enrichment_{timestamp}.csv'
    
    final_df.to_csv(output_file, index=False)
    
    print("=" * 70)
    print("✅ EXPORT COMPLETE!")
    print("=" * 70)
    print()
    print(f"📄 Output File: {output_file}")
    print(f"📊 Total Records: {len(final_df)}")
    print()
    
    # Show sample
    print("📋 SAMPLE DATA (first 3 rows):")
    print()
    print(final_df[['First_Name', 'Last_Name', 'Address', 'Municipality', 'Annual_Tax_Savings']].head(3).to_string())
    print()
    
    # Statistics
    print("=" * 70)
    print("📈 STATISTICS")
    print("=" * 70)
    print()
    print(f"Properties by Municipality:")
    print(final_df['Municipality'].value_counts().to_string())
    print()
    print(f"Total Potential Savings: ${final_df['Annual_Tax_Savings'].sum():,.0f}/year")
    print(f"Average Savings per Property: ${final_df['Annual_Tax_Savings'].mean():,.0f}/year")
    print(f"Highest Savings Opportunity: ${final_df['Annual_Tax_Savings'].max():,.0f}/year")
    print()
    
    print("=" * 70)
    print("🚀 NEXT STEPS")
    print("=" * 70)
    print()
    print("1️⃣  Upload to Skip Tracing Service:")
    print("    • Recommended: BatchSkipTracing.com")
    print("    • Cost: ~$0.10-0.20 per record")
    print(f"    • Your Cost: ~${len(final_df) * 0.15:.2f}")
    print()
    print("2️⃣  Services to Try:")
    print("    • https://batchskiptracing.com (Best overall)")
    print("    • https://ididata.com (Most accurate)")
    print("    • https://batchleads.io (Real estate focused)")
    print()
    print("3️⃣  What You'll Get Back:")
    print("    • Email addresses (70-85% match rate)")
    print("    • Phone numbers (mobile + landline)")
    print("    • Sometimes: LinkedIn, relatives, other addresses")
    print()
    print("4️⃣  Import Enriched Data:")
    print("    • We can build an import tool")
    print("    • Add emails/phones to property detail pages")
    print("    • Add 'Email Owner' and 'Call Owner' buttons")
    print()
    print("=" * 70)
    print()
    print(f"✅ Your enrichment file is ready: {output_file}")
    print()

if __name__ == "__main__":
    export_for_enrichment()

