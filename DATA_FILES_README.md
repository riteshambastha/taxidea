# Data Files

## ⚠️ Data Files Not Included in Git

The source data files are **too large for GitHub** (100MB+ each) and are excluded from this repository:

- `Sales2025.txt` (109 MB) - NJ Sales records (SR1A format)
- `modiv-2025/` folder - County assessment files (MOD IV format)
  - Bergen.txt (190 MB)
  - Ocean.txt (202 MB)
  - Monmouth.txt (172 MB)
  - Middlesex.txt (168 MB)
  - And 17 other county files

## 📁 What IS Included

✅ **All generated leads** (CSV files):
- `marlboro_goldilocks_leads.csv`
- `wall_goldilocks_leads.csv`
- `middletown_goldilocks_leads.csv`

✅ **All Python scripts**:
- `tax_appeal_pipeline.py` - Main analysis pipeline
- `export_for_enrichment.py` - Contact enrichment export
- `app.py` - Web platform
- And all helper scripts

✅ **All documentation**:
- Complete guides and README files
- Property detail templates
- Municipality codes

## 🔧 To Run the Pipeline

If you need to run the analysis:

1. **Get the source data files** from the NJ Department of Treasury:
   - MOD IV files: County property assessments
   - SR1A files: County sales records

2. **Place them in your project:**
   ```
   taxidea/
   ├── Sales2025.txt (SR1A file)
   └── modiv-2025/
       └── Monmouth.txt (or other counties)
   ```

3. **Run the pipeline:**
   ```bash
   python3 tax_appeal_pipeline.py
   ```

## 💡 Alternative: Use Existing Leads

If you just want to use the platform with existing leads:
1. The lead CSV files are already included
2. Just run the web platform:
   ```bash
   ./start_server.sh
   ```
3. Visit: http://localhost:5001

No source data files needed!

## 📊 Data File Locations (If You Have Them)

```
taxidea/
├── Sales2025.txt              # ← Place SR1A file here
├── modiv-2025/                # ← Create this folder
│   ├── Monmouth.txt          # ← Place county files here
│   ├── Middlesex.txt
│   └── ...
```

## ℹ️ Why Not in Git?

GitHub has a 100MB file size limit. Since these are public data files that:
1. Can be obtained from NJ Treasury
2. Are very large (100-200MB each)
3. Change periodically (annual updates)

It makes sense to exclude them and document where to get them instead.

