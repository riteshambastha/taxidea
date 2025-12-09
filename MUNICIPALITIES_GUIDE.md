# Managing Municipalities in TaxIdea Platform

## 🗺️ Current Status

**Platform supports:** 34 NJ municipalities across 8 counties
**Currently loaded:** 2 municipalities with data
- ✅ Marlboro, Monmouth County (20 leads)
- ✅ Wall, Monmouth County (107 leads)

**Pending analysis:** 31 municipalities (shown in dropdown but no data yet)

---

## 📋 All Available Municipalities

### Monmouth County (County Code 13)
- ✅ **Marlboro** (District 28) - 20 leads
- ✅ **Wall** (District 32) - 107 leads
- ⏳ Middletown (District 21)
- ⏳ Howell (District 17)
- ⏳ Ocean (District 30)

### Middlesex County (County Code 12)
- ⏳ East Brunswick (District 04)
- ⏳ Woodbridge (District 25)
- ⏳ Edison (District 05)
- ⏳ Monroe (District 12)

### Bergen County (County Code 02)
- ⏳ Teaneck (District 60)
- ⏳ Fair Lawn (District 17)
- ⏳ Paramus (District 33)
- ⏳ Hackensack (District 23)

### Essex County (County Code 07)
- ⏳ Newark (District 14)
- ⏳ West Orange (District 22)
- ⏳ Bloomfield (District 02)
- ⏳ Livingston (District 10)

### Morris County (County Code 14)
- ⏳ Parsippany-Troy Hills (District 29)
- ⏳ Randolph (District 35)
- ⏳ Rockaway (District 36)
- ⏳ Morris (District 27)

### Somerset County (County Code 18)
- ⏳ Franklin (District 08)
- ⏳ Bridgewater (District 06)
- ⏳ Hillsborough (District 10)

### Union County (County Code 20)
- ⏳ Elizabeth (District 04)
- ⏳ Union (District 19)
- ⏳ Linden (District 09)

### Ocean County (County Code 15)
- ⏳ Brick (District 03)
- ⏳ Jackson (District 05)
- ⏳ Toms River (District 12)

### Passaic County (County Code 16)
- ⏳ Wayne (District 35)
- ⏳ Clifton (District 18)
- ⏳ Paterson (District 27)

---

## 🚀 How to Add a New Municipality

### Method 1: Using the Helper Script (Easiest)

```bash
./add_municipality.sh COUNTY DISTRICT NAME

# Examples:
./add_municipality.sh 12 04 "East Brunswick"
./add_municipality.sh 02 60 Teaneck
./add_municipality.sh 07 22 "West Orange"
```

The script will:
1. Update configuration automatically
2. Run the Goldilocks analysis
3. Generate the CSV file
4. Tell you to restart the server

### Method 2: Manual Process

**Step 1: Edit tax_appeal_pipeline.py**
```python
TARGET_COUNTY = '12'    # Change to your county code
TARGET_DISTRICT = '04'  # Change to your district code
```

Also update these lines:
```python
modiv_file = '/Users/riteshambastha/projects/taxidea/modiv-2025/Middlesex.txt'  # County name
output_file = 'east_brunswick_goldilocks_leads.csv'  # Municipality name
```

**Step 2: Run the analysis**
```bash
python3 tax_appeal_pipeline.py
```

**Step 3: Verify the output**
```bash
ls -lh *_goldilocks_leads.csv
```

**Step 4: Restart the web server**
```bash
./start_server.sh
```

The new municipality will automatically appear in the dropdown!

---

## 🔍 Finding County & District Codes

### Quick Reference: County Codes
```
01 = Atlantic    08 = Gloucester   15 = Ocean
02 = Bergen      09 = Hudson       16 = Passaic
03 = Burlington  10 = Hunterdon    17 = Salem
04 = Camden      11 = Mercer       18 = Somerset
05 = Cape May    12 = Middlesex    19 = Sussex
06 = Cumberland  13 = Monmouth     20 = Union
07 = Essex       14 = Morris       21 = Warren
```

### Finding District Codes

**Method 1: Check the data file**
```bash
# Example: Find districts in Bergen County
grep "^02" modiv-2025/Bergen.txt | cut -c1-4 | sort | uniq -c | sort -rn | head -10
```

Output shows:
```
  12141 0260    ← District 60 (Teaneck)
  11301 0217    ← District 17 (Fair Lawn)
  10434 0233    ← District 33 (Paramus)
```

**Method 2: Use MOD IV file with known address**
```bash
grep -i "MAIN STREET" modiv-2025/Bergen.txt | head -1
```

Look at first 4 characters: `0260` = County 02, District 60

**Method 3: County Website**
Most NJ counties publish district/municipality codes on their tax assessor websites.

---

## 📊 What Happens When You Add a Municipality

### 1. Analysis Process
- Parses MOD IV assessment file for that county/district
- Parses SR1A sales file for that county/district
- Applies Goldilocks filters:
  - ✓ NU Code 0 only (arm's-length sales)
  - ✓ Sale price ≥ $200,000
  - ✓ Ratio 1.15-2.5
  - ✓ Residential only (Class 2)
- Generates CSV with all leads

### 2. Expected Results
Typical yields per municipality:
- **Small towns** (5,000-10,000 properties): 5-20 leads
- **Medium towns** (10,000-20,000 properties): 20-50 leads
- **Large towns** (20,000+ properties): 50-150 leads

### 3. Auto-Loading
Once CSV exists, platform automatically:
- Loads data on server startup
- Adds to dropdown menu
- Enables filtering by that municipality
- Includes in dashboard analytics

---

## 🎯 Recommended Expansion Strategy

### Phase 1: High-Value Suburbs (Start Here)
Target affluent suburbs with high property values:
1. Marlboro, Monmouth ✅ (Done - 20 leads)
2. Wall, Monmouth ✅ (Done - 107 leads)
3. East Brunswick, Middlesex
4. Livingston, Essex
5. Wayne, Passaic
6. Bridgewater, Somerset

**Why?** Higher property values = larger dollar savings = easier to sell

### Phase 2: Large Population Centers
Cover major towns for volume:
1. Woodbridge, Middlesex (largest in NJ)
2. Edison, Middlesex
3. Toms River, Ocean
4. Newark, Essex

**Why?** More properties = more leads = more opportunities

### Phase 3: Additional Coverage
Fill in remaining municipalities as needed based on:
- Your target market
- Geographic proximity
- Referral opportunities

---

## ⚙️ Automation Options

### Batch Analysis Script
To analyze multiple municipalities at once:

```bash
# Create a list
cat > municipalities.txt << EOF
13 32 Wall
12 04 East Brunswick
02 60 Teaneck
07 22 West Orange
EOF

# Run batch
while IFS=' ' read -r county district name; do
    ./add_municipality.sh "$county" "$district" "$name"
    sleep 2
done < municipalities.txt
```

### Scheduled Updates
To refresh data monthly:

```bash
# Add to crontab (crontab -e)
0 2 1 * * cd /Users/riteshambastha/projects/taxidea && ./update_all_municipalities.sh
```

---

## 📈 Analytics by Municipality

Once multiple municipalities are loaded, the dashboard shows:
- **Properties by Municipality** chart
- **Revenue by Municipality** breakdown
- **Best Opportunities per Town**
- **Comparative Analysis** across regions

---

## 🔧 Troubleshooting

### "No leads found for [Municipality]"
**Possible causes:**
1. District code is wrong
2. No properties sold in Goldilocks range
3. All sales have non-usable codes (not NU Code 0)
4. No residential properties in that district

**Solution:** 
- Verify district code
- Try neighboring districts
- Check raw data: `grep "^[COUNTY][DISTRICT]" modiv-2025/[County].txt | wc -l`

### "Municipality not appearing in dropdown"
**Causes:**
1. CSV file doesn't exist
2. Server not restarted
3. app.py not updated

**Solution:**
1. Check: `ls *_goldilocks_leads.csv`
2. Restart: `./start_server.sh`
3. Verify app.py municipalities dict includes it

### "Wrong number of leads"
**Causes:**
- Incorrect district code analyzing wrong town
- Different filters than expected

**Solution:**
- Double-check district code matches actual municipality
- Review filter criteria in tax_appeal_pipeline.py

---

## 🎓 Advanced: Adding Custom Municipality

If you need a municipality not in the list:

**Step 1: Find the codes**
```bash
grep -i "YOUR_TOWN_NAME" modiv-2025/[County].txt | head -1
# Look at first 4 chars for county+district
```

**Step 2: Add to app.py**
```python
municipalities = {
    # ... existing entries ...
    '12-99': {'name': 'Your Town', 'county': 'Middlesex', 'file': 'your_town_goldilocks_leads.csv'},
}
```

**Step 3: Analyze**
```bash
./add_municipality.sh 12 99 "Your Town"
```

**Step 4: Restart**
```bash
./start_server.sh
```

---

## 📝 Quick Commands Reference

```bash
# Add a municipality
./add_municipality.sh COUNTY DISTRICT "NAME"

# List all CSV files (shows what's loaded)
ls -lh *_goldilocks_leads.csv

# Check a specific municipality's lead count
wc -l marlboro_goldilocks_leads.csv

# Restart server to load new data
./start_server.sh

# Find district codes for a county
grep "^13" modiv-2025/Monmouth.txt | cut -c1-4 | sort | uniq -c | sort -rn | head -10

# Search for a specific town in data
grep -i "MARLBORO" modiv-2025/Monmouth.txt | head -1
```

---

## 🎯 Your Current Status

✅ **Ready to Use:**
- Marlboro (20 leads, $761K opportunity)
- Wall (107 leads, checking opportunity)

⏳ **Ready to Add:**
- 31 municipalities defined in dropdown
- Just run analysis for each one
- Use `./add_municipality.sh` script

🚀 **Next Steps:**
1. Pick 3-5 target municipalities
2. Run `./add_municipality.sh` for each
3. Restart server
4. Start finding clients!

---

**Access your platform:** http://localhost:5001

**View all municipalities:** http://localhost:5001/search
(Dropdown now shows all 34 options!)

