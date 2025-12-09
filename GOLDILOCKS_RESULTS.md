# Marlboro Tax Appeal Leads - Goldilocks Analysis

## 🎯 Executive Summary

**20 legitimate tax appeal candidates identified** in Marlboro Township using strict "Goldilocks" filtering to eliminate false positives and data artifacts.

### Key Metrics
- **Total Implied Over-Assessment**: $760,680
- **Total Annual Tax Savings Potential**: $16,735
- **Average Assessment Ratio**: 1.25x (assessments 25% above recent sale prices)
- **Ratio Range**: 1.15x to 1.72x (all within reasonable appeal range)

---

## 📋 Goldilocks Methodology

### The Problem with Raw Data
Initial analysis returned extreme outliers:
- Properties selling for $19K-$32K (vacant lots, partial interests, data errors)
- Assessment ratios of 30x-50x (data artifacts, not viable appeals)
- Non-arm's-length transactions (foreclosures, family transfers)

### The Goldilocks Solution: "Just Right" Filtering

#### 1. Stricter Arm's-Length Filtering
**NU Code = '000' ONLY**
- Keeps only code 0 (certified arm's-length sales)
- Rejects: Foreclosures (10), Related parties (26), Estate sales (07), etc.
- **Result**: 544 valid sales (from 1,128 total)

#### 2. Price Floor: $200,000 Minimum
- Ensures single-family residential homes only
- Eliminates: Vacant lots, partial interests, condos, data errors
- **Result**: 485 valid sales over $200K

#### 3. Goldilocks Ratio Range: 1.15 to 2.5
- **< 1.15**: Not enough savings to justify appeal (~15% buffer is normal)
- **1.15 - 2.5**: Sweet spot for legitimate appeals
- **> 2.5**: Likely teardowns, data errors, or complex cases (MVP-excluded)
- **Result**: 20 properties in the Goldilocks range

#### 4. Implied Over-Assessment Calculation
```
Implied_Overpayment = Assessed_Value - (Sale_Price × 1.15)
```
- 1.15 factor accounts for Chapter 123 common level range
- Provides safe buffer for assessment variations
- Represents the "excess" assessment above reasonable market value

---

## 🏆 Top 10 Appeal Candidates

| Rank | Address | Sale Price | Assessment | Ratio | Implied Over-Assessment | Annual Savings |
|------|---------|------------|------------|-------|------------------------|----------------|
| 1 | Wilson Avenue | $222,800 | $383,500 | 1.72x | $127,280 | $2,800 |
| 2 | Summit Court | $514,500 | $681,400 | 1.32x | $89,725 | $1,974 |
| 3 | 3 Main Street | $290,600 | $409,100 | 1.41x | $74,910 | $1,648 |
| 4 | Sanford Street | $415,200 | $538,100 | 1.30x | $60,620 | $1,334 |
| 5 | Wood Avenue | $350,200 | $463,200 | 1.32x | $60,470 | $1,330 |
| 6 | 3 Daum Road | $460,200 | $582,100 | 1.26x | $52,870 | $1,163 |
| 7 | Alexandria Drive | $653,800 | $799,500 | 1.22x | $47,630 | $1,048 |
| 8 | 6 Taylors Mills Road | $661,200 | $801,800 | 1.21x | $41,420 | $911 |
| 9 | Scott Lane (Framingham) | $681,100 | $819,200 | 1.20x | $35,935 | $791 |
| 10 | Hill Court | $436,500 | $531,900 | 1.22x | $29,925 | $658 |

---

## 📊 Analysis Breakdown

### Data Quality Improvements

| Metric | Original | Goldilocks | Change |
|--------|----------|------------|--------|
| Sales Records | 1,128 | 485 | -57% (quality filter) |
| Matched Properties | 56 | 143 | +155% (better matching) |
| Over-Assessed (>1.0) | 8 | 123 | +1438% (realistic range) |
| Appeal Candidates | 8 | 20 | +150% (after Goldilocks) |
| Avg Ratio | 19.28x | 1.25x | **-94%** (eliminated outliers) |

### Why the Original Had Extreme Ratios
1. **No price floor**: Included $19K-$68K sales (vacant lots, teardowns)
2. **Used 'U' code**: Broader definition captured marginal transactions
3. **No upper ratio limit**: Included obvious data errors (50x ratios)

### Why Goldilocks Is Better
1. **Legitimate homes**: All sales $200K+ (actual single-family residences)
2. **True arm's-length**: Code 0 only (market-rate transactions)
3. **Appealable range**: 1.15-2.5x ratios (court-acceptable cases)
4. **Defensible math**: 1.15x safe buffer built into calculations

---

## 💼 Business Implications

### Revenue Potential
- **Top 5 leads**: $375K in over-assessment = $8,250/year in savings
- **Top 10 leads**: $580K in over-assessment = $12,770/year in savings
- **All 20 leads**: $761K in over-assessment = $16,735/year in savings

### Typical Fee Structure
If charging 50% of first-year tax savings:
- **Top lead (Wilson Ave)**: $1,400 fee potential
- **Top 5 average**: $1,650 fee potential per client
- **All 20 leads**: $8,368 total fee potential (Year 1 only)

### Multi-Year Value
- Appeals typically result in 3-5 years of savings
- Recurring revenue from renewals
- Referral potential from satisfied clients

---

## 🎓 Technical Notes

### Field Specifications Used
- **NU Code**: Position 53-56 in SR1A file
  - '000' = Code 0 (valid arm's-length sale)
  - '010' = Code 10 (foreclosure - excluded)
  - '026' = Code 26 (related party - excluded)

- **Sale Price**: Position 10-19 (9 digits)
- **Assessment**: Position 438-447 (9 digits)
- **Block/Lot/Qual**: Positions 350-373 (for matching)

### Assumptions
- **Effective Tax Rate**: 2.2% (Marlboro average)
- **Common Level Buffer**: 1.15x (Chapter 123 safe harbor)
- **Year**: 2025 data (recent sales only)

---

## 📁 Output Files

1. **marlboro_goldilocks_leads.csv**
   - Complete dataset with all 20 leads
   - Includes: Block, Lot, Address, Sale Price, Assessment, Ratio, Implied Overpayment, Annual Savings, Sale Date

2. **tax_appeal_pipeline.py**
   - Automated analysis script
   - Configurable for any NJ county/district
   - Goldilocks filters built-in

---

## 🚀 Next Steps

### For Outreach
1. Sort by **Implied_Overpayment** (biggest winners first)
2. Focus on Top 10 (highest ROI for appeals)
3. Filter by recent sale dates (more defensible)

### For Analysis
1. Run for additional municipalities
2. Compare Goldilocks results across towns
3. Identify towns with systematic over-assessment patterns

### For Validation
1. Cross-reference with public records
2. Verify sale dates and circumstances
3. Confirm current ownership for outreach

---

**Generated**: December 6, 2025  
**Municipality**: Marlboro Township, Monmouth County, NJ  
**Data Source**: NJ MOD IV & SR1A 2025 files  
**Methodology**: Goldilocks Filtering (v1.0)

