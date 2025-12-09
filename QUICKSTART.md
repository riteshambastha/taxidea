# TaxIdea Platform - Quick Start Guide

## 🚀 Your Web Platform is Running!

**Access it here:** http://localhost:5001

---

## 📱 Platform Pages

### 1. **Home Page** (http://localhost:5001/)
- Overview of all tax appeal opportunities
- Key statistics dashboard
- Methodology explanation
- Quick navigation to search and analytics

### 2. **Search Properties** (http://localhost:5001/search)
**Filter Options:**
- Municipality (currently: Marlboro)
- Minimum annual savings (e.g., $500+)
- Sale price range (e.g., $300K-$700K)
- Assessment ratio (Goldilocks: 1.15-2.5)

**Sort By:**
- Implied over-assessment (default - biggest opportunities first)
- Assessment ratio
- Annual tax savings
- Sale price

**Example Searches:**
```
Find properties with $1,000+ annual savings:
http://localhost:5001/search?min_savings=1000

Find properties in $400K-$600K price range:
http://localhost:5001/search?min_price=400000&max_price=600000

Find highest ratio properties:
http://localhost:5001/search?sort=Ratio
```

### 3. **Property Details** (Click any property from search)
Each property page shows:
- ✅ Recent sale price and date
- ✅ Current assessment
- ✅ Assessment ratio (how many times over sale price)
- ✅ Implied over-assessment ($ amount)
- ✅ Annual tax savings potential
- ✅ 3-year and 5-year savings projections
- ✅ Fee opportunity (50% of Year 1 savings)
- ✅ Outreach checklist

**Example:**
```
Wilson Avenue property:
http://localhost:5001/property/13-28/00047/00005

Shows:
• Sale Price: $222,800
• Assessment: $383,500
• Ratio: 1.72x
• Annual Savings: $2,800
• Fee Opportunity: $1,400
```

### 4. **Analytics Dashboard** (http://localhost:5001/dashboard)
**Visualizations:**
- Distribution by assessment ratio
- Distribution by sale price
- Top 10 opportunities table
- Revenue potential calculator
- Data quality metrics

---

## 💡 Common Workflows

### Workflow 1: Find Your Top Leads
1. Go to Dashboard → View top 10 opportunities
2. Click on #1 property → Review full details
3. Note owner name and address
4. Use outreach checklist on property page

### Workflow 2: Filter for Specific Client Type
1. Go to Search page
2. Set filters:
   - Min Savings: $1,000 (serious opportunities)
   - Min Price: $400,000 (higher-value homes)
   - Max Ratio: 2.0 (exclude extreme cases)
3. Review results
4. Click property details for each lead

### Workflow 3: Analyze Market Opportunity
1. Go to Dashboard
2. Review ratio distribution chart
3. Check price range distribution
4. Note total opportunity value
5. Calculate revenue potential (50% fees)

---

## 🎯 Sample Use Cases

### Finding Properties for Outreach
**Goal:** Get 10 leads for this week's outreach

**Steps:**
1. Dashboard → Top 10 table
2. Click each property
3. Export details (copy/paste for now)
4. Focus on properties with:
   - $1,000+ annual savings
   - Recent sales (2024-2025)
   - Clear owner information

### Analyzing a Specific Property
**Goal:** Determine if Wilson Avenue is worth pursuing

**Steps:**
1. Search → Find "Wilson Avenue"
2. Click for details
3. Review:
   - Assessment: $383,500
   - Sale: $222,800 (May 2025)
   - Ratio: 1.72x ✅ (Goldilocks range)
   - Annual Savings: $2,800
   - Owner: [Listed on page]
4. Decision: **YES** - Strong candidate!

### Calculating Your Revenue
**Goal:** Estimate monthly revenue from current leads

**Steps:**
1. Dashboard → Revenue Potential section
2. Top 10 leads = $8,368 potential (Year 1, 50% fees)
3. If converting 5 out of 10 = $4,184
4. Spread over 3 months = ~$1,400/month
5. With 3-year appeals = sustained revenue

---

## 🔧 Platform Management

### Adding New Municipalities

**Step 1:** Run analysis for new town
```bash
# Edit tax_appeal_pipeline.py
TARGET_COUNTY = '12'    # Middlesex
TARGET_DISTRICT = '04'  # East Brunswick

# Run analysis
python3 tax_appeal_pipeline.py
```

**Step 2:** Update app.py
```python
municipalities = {
    '13-28': {'name': 'Marlboro', 'county': 'Monmouth', 
              'file': 'marlboro_goldilocks_leads.csv'},
    '12-04': {'name': 'East Brunswick', 'county': 'Middlesex', 
              'file': 'east_brunswick_goldilocks_leads.csv'},
}
```

**Step 3:** Restart server
```bash
./start_server.sh
```

### Updating Data

When new MOD IV and SR1A files arrive:
```bash
# 1. Place new files in project directory
# 2. Run analysis
python3 tax_appeal_pipeline.py

# 3. Restart server (auto-loads new data)
./start_server.sh
```

---

## 📊 Understanding the Data

### Goldilocks Methodology

**Why "Goldilocks"?**
- **< 1.15**: Too small - within normal variance, not worth appeal
- **1.15-2.5**: Just right - legitimate appeal opportunities
- **> 2.5**: Too large - likely data errors or teardowns

**Example:**
- Sale Price: $500,000
- Assessment: $625,000
- Ratio: 1.25x ✅ (in Goldilocks range)
- Implied Over-Assessment: $50,000
  - Calculation: $625K - ($500K × 1.15) = $50K
- Annual Tax Savings: $1,100
  - Calculation: $50K × 2.2% tax rate = $1,100

### Data Quality Filters

All properties in platform have:
1. ✅ NU Code 0 (verified arm's-length sale)
2. ✅ Sale Price ≥ $200,000 (real homes, not lots)
3. ✅ Ratio 1.15-2.5 (Goldilocks range)
4. ✅ Residential property (Class 2)
5. ✅ Recent sale with assessment data

---

## 💼 Business Tips

### Prioritizing Leads

**Tier 1 (Immediate Contact):**
- Annual savings > $2,000
- Recent sales (last 6 months)
- Clear owner information

**Tier 2 (Follow-up):**
- Annual savings $1,000-$2,000
- Sales within last year
- Owner name available

**Tier 3 (Long-term):**
- Annual savings $500-$1,000
- Older sales (12+ months)
- Research owner needed

### Pitch Template

Use property details page to create pitch:
```
Hi [Owner Name],

I noticed your property at [Address] recently sold for 
[$Sale_Price] in [Month/Year], but is currently assessed 
at [$Assessment].

This means you may be overpaying approximately [$Annual_Savings] 
per year in property taxes.

We specialize in property tax appeals and work on a 
contingency basis - you only pay if we save you money.

Would you be interested in a free evaluation?
```

---

## 🆘 Troubleshooting

### Can't Access Website
**Check:** Is server running?
```bash
ps aux | grep "python3 app.py"
```

**Fix:** Restart server
```bash
./start_server.sh
```

### No Properties Showing
**Check:** Is CSV file present?
```bash
ls -la marlboro_goldilocks_leads.csv
```

**Fix:** Run analysis first
```bash
python3 tax_appeal_pipeline.py
```

### Port Already in Use
**Fix:** Change port in app.py (line ~370)
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Try 5002
```

---

## 📞 Next Steps

1. ✅ **Explore Platform** - Browse all pages
2. ✅ **Identify Top 10** - Review best opportunities
3. ✅ **Plan Outreach** - Create contact list
4. ✅ **Track Results** - Monitor conversion rates
5. ✅ **Expand Coverage** - Add more municipalities

---

## 🔗 Quick Links

| Page | URL |
|------|-----|
| Home | http://localhost:5001/ |
| Search | http://localhost:5001/search |
| Dashboard | http://localhost:5001/dashboard |
| Top Lead | http://localhost:5001/property/13-28/00047/00005 |

---

**Happy Lead Hunting! 🎯**

Your tax appeal platform is ready to help you find and contact property owners who are overpaying on their taxes.

For detailed documentation, see: `WEB_PLATFORM_README.md`

