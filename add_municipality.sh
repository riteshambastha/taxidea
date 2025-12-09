#!/bin/bash

# Quick script to analyze a new municipality
# Usage: ./add_municipality.sh COUNTY DISTRICT NAME

if [ $# -lt 3 ]; then
    echo "Usage: ./add_municipality.sh COUNTY DISTRICT NAME"
    echo ""
    echo "Examples:"
    echo "  ./add_municipality.sh 13 32 Wall"
    echo "  ./add_municipality.sh 12 04 'East Brunswick'"
    echo "  ./add_municipality.sh 02 60 Teaneck"
    echo ""
    echo "Common Counties:"
    echo "  02 = Bergen"
    echo "  07 = Essex"
    echo "  12 = Middlesex"
    echo "  13 = Monmouth"
    echo "  14 = Morris"
    echo "  15 = Ocean"
    echo "  16 = Passaic"
    echo "  18 = Somerset"
    echo "  20 = Union"
    exit 1
fi

COUNTY=$1
DISTRICT=$2
NAME=$3

# Determine county name
case $COUNTY in
    "01") COUNTY_NAME="Atlantic" ;;
    "02") COUNTY_NAME="Bergen" ;;
    "03") COUNTY_NAME="Burlington" ;;
    "04") COUNTY_NAME="Camden" ;;
    "05") COUNTY_NAME="Cape May" ;;
    "06") COUNTY_NAME="Cumberland" ;;
    "07") COUNTY_NAME="Essex" ;;
    "08") COUNTY_NAME="Gloucester" ;;
    "09") COUNTY_NAME="Hudson" ;;
    "10") COUNTY_NAME="Hunterdon" ;;
    "11") COUNTY_NAME="Mercer" ;;
    "12") COUNTY_NAME="Middlesex" ;;
    "13") COUNTY_NAME="Monmouth" ;;
    "14") COUNTY_NAME="Morris" ;;
    "15") COUNTY_NAME="Ocean" ;;
    "16") COUNTY_NAME="Passaic" ;;
    "17") COUNTY_NAME="Salem" ;;
    "18") COUNTY_NAME="Somerset" ;;
    "19") COUNTY_NAME="Sussex" ;;
    "20") COUNTY_NAME="Union" ;;
    "21") COUNTY_NAME="Warren" ;;
    *) echo "Unknown county code: $COUNTY"; exit 1 ;;
esac

SAFE_NAME=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | tr '-' '_')
OUTPUT_FILE="${SAFE_NAME}_goldilocks_leads.csv"

echo "========================================"
echo "Analyzing: $NAME"
echo "========================================"
echo "County: $COUNTY_NAME (Code $COUNTY)"
echo "District: $DISTRICT"
echo "Output: $OUTPUT_FILE"
echo ""

# Update tax_appeal_pipeline.py
sed -i.bak "s/TARGET_COUNTY = '[0-9]*'/TARGET_COUNTY = '$COUNTY'/" tax_appeal_pipeline.py
sed -i.bak "s/TARGET_DISTRICT = '[0-9]*'/TARGET_DISTRICT = '$DISTRICT'/" tax_appeal_pipeline.py
sed -i.bak "s|modiv-2025/[A-Za-z]*\.txt|modiv-2025/$COUNTY_NAME.txt|" tax_appeal_pipeline.py
sed -i.bak "s/output_file = '.*_goldilocks_leads\.csv'/output_file = '$OUTPUT_FILE'/" tax_appeal_pipeline.py

echo "Running analysis..."
python3 tax_appeal_pipeline.py

if [ -f "$OUTPUT_FILE" ]; then
    COUNT=$(wc -l < "$OUTPUT_FILE")
    COUNT=$((COUNT - 1))  # Subtract header
    echo ""
    echo "✅ Success! Found $COUNT leads in $OUTPUT_FILE"
    echo ""
    echo "Next steps:"
    echo "1. Restart the web server: ./start_server.sh"
    echo "2. The municipality will appear in the dropdown"
else
    echo ""
    echo "❌ No leads file generated. Check the output above for errors."
fi

# Cleanup backup files
rm -f tax_appeal_pipeline.py.bak

