# NJ Property Tax Appeal Lead Generator

## Overview
This Python pipeline analyzes NJ property assessment and sales data to identify properties that are over-assessed relative to their recent sale prices. These properties are prime candidates for property tax appeals.

## Files
- `tax_appeal_pipeline.py` - Main analysis script
- `marlboro_leads.csv` - Output file with identified leads
- `modiv-2025/` - Assessment data (MOD IV format)
- `Sales2025.txt` - Sales transaction data (SR1A format)

## How It Works

### Step 1: Data Ingestion
The script parses two fixed-width legacy mainframe files:
- **MOD IV**: Property assessments with owner info, addresses, and taxable values
- **SR1A**: Sales records with prices, dates, and transaction codes

### Step 2: Filtering ("The Secret Sauce")
Applies strict filters to ensure data quality:
- **Geography**: Monmouth County (13), Marlboro Township (28)
- **Property Class**: Residential only (Class 2)
- **Transaction Type**: Arm's-length sales only (NU Code 'U')
  - Excludes: Foreclosures (N10), Related parties (N26), Estate sales (N07), etc.

### Step 3: The Calculation
- Merges sales and assessment data on Block/Lot/Qualifier
- Calculates Ratio = Assessed Value / Sale Price
- Estimates annual tax overpayment (assumes 2.2% effective tax rate)

### Step 4: Identify "Victims"
- Filters for Ratio > 1.0 (assessment exceeds sale price)
- Sorts by ratio descending (worst cases first)
- Outputs to CSV with full details

## Configuration
Edit these variables at the top of `tax_appeal_pipeline.py` to target different areas:

```python
TARGET_COUNTY = '13'    # Monmouth County
TARGET_DISTRICT = '28'  # Marlboro Township
```

## Usage

```bash
python3 tax_appeal_pipeline.py
```

The script will:
1. Parse and filter the data
2. Generate `marlboro_leads.csv`
3. Display top 10 worst over-assessments in console

## Output Format

The CSV contains:
- **Block/Lot**: Property identifier
- **Address**: Property location
- **Sale_Price**: Recent sale price
- **Assessed_Value**: Current tax assessment
- **Ratio**: Assessment-to-sale ratio (>1.0 = over-assessed)
- **Potential_Overpayment**: Estimated annual tax overpayment
- **Sale_Date**: Date of sale (MMDDYY format)
- **Owner_Name**: Property owner

## Results for Marlboro

**8 over-assessed properties identified**

Top 3 Leads:
1. **Fallswood Lane**: Sold for $19K, assessed at $1.02M (53x ratio) - $22K/year overpayment
2. **Bloomfield Road (Player)**: Sold for $30K, assessed at $1.03M (34x ratio) - $22K/year overpayment
3. **Queen Court**: Sold for $32K, assessed at $1.03M (32x ratio) - $22K/year overpayment

**Total potential tax savings: $176,000/year**

## Notes

- These extreme cases (50x+ ratios) are likely vacant lots, teardowns, or distressed sales
- The town's assessment hasn't been updated to reflect the reduced value
- All transactions are verified arm's-length sales (NU Code 'U')
- Perfect candidates for tax appeals

## Field Specifications

### MOD IV (Assessment) Layout
- County: 1-2
- District: 3-4
- Block: 5-13
- Lot: 14-22
- Qualifier: 23-27
- Property Class: 57 (single digit)
- Address: 61-95
- Net Taxable Value: 439-447

### SR1A (Sales) Layout  
- County: 1-2
- District: 3-4
- Sale Price: 11-19 (early in record)
- Sale Date: 20-25 (MMDDYY)
- NU Code: 34-36 ('U' = usable sale)
- Block: 351-359 (late in record)
- Lot: 360-368
- Qualifier: 369-373

## Requirements
```bash
pip install pandas
```

## License
Proprietary - For internal use only

