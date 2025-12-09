# Contact Information Enrichment Guide

## 📧 Getting Names & Email Addresses for Property Owners

---

## ✅ What We Already Have

### From MOD IV (Assessment Records):
- ✓ **Property Address** (55-84) - Full street address
- ✓ **Owner Name** (Position 200-250) - Property owner's name on tax records
- ✓ **Block, Lot, Qual** - Unique property identifier

### Currently Displayed:
- Owner names are captured in the CSV output
- Shown on property detail pages (when available)
- Public record data (legally obtainable)

---

## ❌ What We DON'T Have

- ✗ **Email addresses** - Not in public tax records
- ✗ **Phone numbers** - Not in our data source
- ✗ **Mailing addresses** (if different from property)
- ✗ **Multiple owners** (only primary shown)

---

## 🔍 Options for Getting Email Addresses

### Option 1: **Skip Tracing Services** (Real Estate Focused)
**Best for:** Bulk contact data enrichment

**Services:**
- **BatchSkipTracing** - https://batchskiptracing.com
  - Cost: ~$0.10-0.20 per record
  - Returns: Email, phone, relatives, liens
  - Upload CSV, get enriched CSV back
  
- **IDI Data** - https://ididata.com
  - Cost: ~$0.15 per record
  - Very accurate for homeowners
  - Batch processing available

- **BatchLeads** - https://batchleads.io
  - Cost: ~$0.12 per record  
  - Real estate investor focused
  - Good for property owner data

**How It Works:**
1. Export your leads CSV (Block, Lot, Address, Owner_Name)
2. Upload to skip tracing service
3. They match against 200+ data sources
4. Download enriched CSV with emails/phones
5. Import back into your platform

**Pros:**
- ✓ Bulk processing (all 146 leads at once)
- ✓ High accuracy (70-85% match rate)
- ✓ Gets multiple contact methods
- ✓ Relatively cheap ($15-30 for all your current leads)

**Cons:**
- ✗ Costs money (per record)
- ✗ Manual upload/download process
- ✗ Not real-time

---

### Option 2: **API-Based Enrichment** (Automated)
**Best for:** Real-time enrichment as you add properties

**Services:**
- **RocketReach API** - https://rocketreach.co/api
  - Cost: $49/mo for 170 lookups
  - Best: High accuracy, professional emails
  - API integration available

- **Hunter.io** - https://hunter.io
  - Cost: $49/mo for 500 searches
  - Best: Company emails, domain search
  - Good API documentation

- **People Data Labs** - https://peopledatalabs.com
  - Cost: $0.03-0.10 per record (pay as you go)
  - Best: Comprehensive person data
  - Developer-friendly

- **Clearbit** - https://clearbit.com
  - Cost: Custom pricing
  - Best: Tech-savvy users
  - Real-time enrichment

**How It Works:**
```python
# Example integration (RocketReach)
import requests

def enrich_property(owner_name, address, city):
    url = "https://api.rocketreach.co/v2/api/lookupProfile"
    headers = {"Api-Key": "YOUR_API_KEY"}
    params = {
        "name": owner_name,
        "current_employer": address  # Use address as location hint
    }
    response = requests.post(url, headers=headers, json=params)
    data = response.json()
    return data.get('emails', [])
```

**Pros:**
- ✓ Automated (no manual work)
- ✓ Real-time enrichment
- ✓ Integrates into your platform
- ✓ Only pay for what you use

**Cons:**
- ✗ Requires coding
- ✗ Higher per-record cost
- ✗ Monthly subscriptions
- ✗ API rate limits

---

### Option 3: **Manual Lookup** (Free but Time-Consuming)
**Best for:** High-value leads only

**Sources:**
1. **Google Search**
   - Search: "Owner Name" + Address + Email
   - Often finds social profiles, business emails
   
2. **Facebook/LinkedIn**
   - Search by name and location
   - Send connection/friend request
   - Message feature
   
3. **County Tax Records**
   - Some counties list mailing addresses
   - May differ from property address
   - Can mail letters
   
4. **Whitepages.com**
   - Free basic lookup
   - Shows phone numbers (sometimes)
   - Premium = $5/mo for unlimited
   
5. **Been Verified / Spokeo**
   - ~$20/mo subscription
   - Comprehensive background data
   - Manual lookup (one at a time)

**Pros:**
- ✓ Free (or very cheap)
- ✓ No technical setup
- ✓ Can verify accuracy

**Cons:**
- ✗ VERY time-consuming
- ✗ Inconsistent results
- ✗ Not scalable (146 properties = many hours)

---

### Option 4: **Direct Mail** (No Email Needed)
**Best for:** Professional outreach without emails

**Services:**
- **Click2Mail** - https://click2mail.com
  - Upload addresses, they print/mail
  - ~$0.60-1.00 per letter
  
- **PostGrid** - https://postgrid.com
  - API-based direct mail
  - Automate postcards/letters

**Strategy:**
1. Design professional letter/postcard
2. Include your contact info prominently
3. They respond to YOU (phone/email)
4. Build contact list organically

**Sample Letter:**
```
Dear [Owner Name],

I noticed your property at [Address] may be over-assessed
based on your recent purchase price of $[Sale_Price].

You could be entitled to a tax reduction of $[Annual_Tax_Savings]
per year - that's $[5 Year Savings] over 5 years!

We offer a FREE assessment review. No upfront cost.
We only get paid if we save you money.

Call/Text: (XXX) XXX-XXXX
Email: appeals@yourcompany.com

[Your Name]
NJ Licensed Tax Appeal Specialist
```

**Pros:**
- ✓ Professional appearance
- ✓ High response rate (physical mail stands out)
- ✓ No email needed
- ✓ Builds credibility

**Cons:**
- ✗ Costs $90-150 for all 146 leads
- ✗ Slower (1-2 week turnaround)
- ✗ Not trackable (don't know who opened it)

---

## 🎯 Recommended Strategy

### **For Your Current Situation (146 Leads):**

**Phase 1: Quick Win (Today)**
1. Use **BatchSkipTracing** ($15-30 total)
2. Export your 146 leads to CSV
3. Upload for enrichment
4. Get back emails + phones in 24-48 hours

**Phase 2: Automated System (Next Week)**
1. Integrate **People Data Labs API** ($0.03/record)
2. Auto-enrich new properties as you add townships
3. Build contact database over time

**Phase 3: Multi-Channel Outreach**
1. Email to enriched contacts (70-85 responses)
2. Direct mail to non-matches (remaining 20-45)
3. LinkedIn for high-value leads ($10K+ savings)

---

## 💻 Code Implementation

### Option A: Quick CSV Enrichment (Manual)

```python
# export_for_enrichment.py
import pandas as pd

# Load all leads
leads = pd.concat([
    pd.read_csv('marlboro_goldilocks_leads.csv'),
    pd.read_csv('wall_goldilocks_leads.csv'),
    pd.read_csv('middletown_goldilocks_leads.csv')
])

# Prepare for skip tracing service
enrichment_input = leads[['Address', 'Owner_Name', 'Block', 'Lot']].copy()
enrichment_input['City'] = 'Monmouth'  # Add city
enrichment_input['State'] = 'NJ'
enrichment_input['Zip'] = ''  # Can extract if needed

# Save for upload
enrichment_input.to_csv('leads_for_enrichment.csv', index=False)

print(f"✅ Exported {len(enrichment_input)} properties")
print("📤 Upload to BatchSkipTracing.com")
```

### Option B: API Integration (Automated)

```python
# enrich_contacts.py
import pandas as pd
import requests
import time

PEOPLEDATALABS_API_KEY = "YOUR_API_KEY_HERE"

def enrich_contact(owner_name, address, city, state):
    """Enrich a single property owner's contact info"""
    
    url = "https://api.peopledatalabs.com/v5/person/search"
    headers = {"X-Api-Key": PEOPLEDATALABS_API_KEY}
    
    params = {
        "name": owner_name,
        "location": f"{address}, {city}, {state}",
        "min_likelihood": 6  # Only high-confidence matches
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if data.get('status') == 200 and data.get('data'):
            person = data['data'][0]
            return {
                'email': person.get('emails', [{}])[0].get('address'),
                'phone': person.get('phone_numbers', [{}])[0].get('number'),
                'linkedin': person.get('linkedin_url')
            }
    except Exception as e:
        print(f"Error enriching {owner_name}: {e}")
    
    return {'email': None, 'phone': None, 'linkedin': None}

def enrich_all_leads():
    """Enrich all properties in your database"""
    
    # Load leads
    leads = pd.read_csv('marlboro_goldilocks_leads.csv')
    
    # Enrich each one
    enriched = []
    for idx, row in leads.iterrows():
        print(f"Enriching {idx+1}/{len(leads)}: {row['Address']}")
        
        contact = enrich_contact(
            row['Owner_Name'], 
            row['Address'],
            'Marlboro',  # Use actual city
            'NJ'
        )
        
        enriched.append({
            **row,
            'Email': contact['email'],
            'Phone': contact['phone'],
            'LinkedIn': contact['linkedin']
        })
        
        time.sleep(1)  # Rate limiting
    
    # Save enriched data
    enriched_df = pd.DataFrame(enriched)
    enriched_df.to_csv('marlboro_enriched_leads.csv', index=False)
    
    print(f"\n✅ Enriched {len(enriched)} properties")
    print(f"📧 Found {enriched_df['Email'].notna().sum()} emails")
    print(f"📱 Found {enriched_df['Phone'].notna().sum()} phones")

if __name__ == "__main__":
    enrich_all_leads()
```

---

## 📊 Expected Results

### Skip Tracing Services (Batch):
- **Match Rate:** 70-85%
- **Cost:** $15-30 for 146 leads
- **Turnaround:** 24-48 hours
- **Expected Output:**
  - 100-124 emails found
  - 110-130 phone numbers found
  - 20-45 no match

### API Services (Real-time):
- **Match Rate:** 60-75%
- **Cost:** $4-15 for 146 leads
- **Turnaround:** Instant
- **Expected Output:**
  - 88-110 emails found
  - 90-115 phone numbers found
  - 35-60 no match

---

## 🚀 Next Steps

### To Get Started Today:

1. **Export Current Leads:**
   ```bash
   # We can create a script for this
   python export_for_enrichment.py
   ```

2. **Sign Up for Skip Tracing:**
   - Recommended: BatchSkipTracing.com
   - Upload your CSV
   - Cost: ~$20-30

3. **Get Enriched Data Back:**
   - Download enriched CSV
   - Import into platform

4. **Update Platform to Show Contacts:**
   - Add email/phone columns
   - Display on property detail pages
   - Add "Email Owner" button

### Want Me to Build This?

I can add:
- ✅ Export script for enrichment services
- ✅ API integration for automated enrichment
- ✅ Contact display on property pages
- ✅ "Email Owner" and "Call Owner" buttons
- ✅ CRM features (track outreach, responses)

Just let me know which option you prefer!

---

## 📝 Legal Considerations

**✅ Legal:**
- Using public property owner data
- Enriching with commercially available data
- Emailing about tax assessment (legitimate business purpose)
- Following CAN-SPAM Act (unsubscribe option)

**⚠️ Required:**
- Include your business name/address in emails
- Provide unsubscribe mechanism
- Honor opt-out requests within 10 days
- Don't use deceptive subject lines

**Sample Compliant Email:**
```
Subject: Property Tax Reduction Opportunity - [Address]

Dear [Owner Name],

Based on public records, your property at [Address] may be 
over-assessed...

[Your pitch]

---
[Your Company Name]
[Physical Address]
[Phone/Email]

To opt out of future emails: [Unsubscribe Link]
```

---

## Summary

**Fastest/Easiest:** BatchSkipTracing ($20-30, 24-48 hours, 70-85% match rate)
**Most Automated:** People Data Labs API ($5-15, instant, 60-75% match rate)
**Free but Slow:** Manual lookup (free, weeks of work, variable results)
**No Email Needed:** Direct mail ($90-150, professional, high response rate)

**My Recommendation:** Start with BatchSkipTracing to enrich your current 146 leads, then integrate People Data Labs API for future automation.

Would you like me to build the enrichment features into your platform?

