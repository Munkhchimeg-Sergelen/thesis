#!/usr/bin/env python3
"""
Extract transcripts from Mozilla Common Voice Delta dataset
Matches the audio files you already have
"""

import requests
import json
import os
from pathlib import Path
import time

# Dataset IDs from Mozilla Delta
DATASETS = {
    'mn': 'cmflnuzw62lynu310rvwy9yod',  # Mongolian (from your link)
    'hu': None,  # Need to find
    'es': None,  # Need to find  
    'fr': None,  # Need to find
}

def download_delta_metadata(dataset_id, lang):
    """Download metadata JSON from Delta dataset"""
    print(f"\n{'='*60}")
    print(f"Processing {lang.upper()}")
    print(f"{'='*60}")
    
    # Delta API endpoint (you may need to adjust this)
    # The actual API might be different, but we can try the direct dataset page
    url = f"https://datacollective.mozillafoundation.org/datasets/{dataset_id}"
    
    print(f"Fetching metadata from: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✓ Fetched dataset page")
            # Try to find download link or API endpoint
            # This is a placeholder - we need to inspect the actual page structure
            return response.text
        else:
            print(f"❌ Failed: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def extract_from_original_download():
    """
    Alternative: Check if original download files still exist
    Common Voice datasets usually include a TSV file with metadata
    """
    print("\n" + "="*60)
    print("CHECKING FOR ORIGINAL DOWNLOAD METADATA")
    print("="*60)
    
    # Check common locations
    possible_locations = [
        "~/Downloads/common_voice_*/",
        "~/thesis-asr/data/",
        "~/cv-corpus-*/",
    ]
    
    import glob
    for pattern in possible_locations:
        expanded = os.path.expanduser(pattern)
        matches = glob.glob(expanded)
        if matches:
            print(f"Found: {matches}")
            for match in matches:
                # Look for TSV files
                tsv_files = list(Path(match).rglob("*.tsv"))
                if tsv_files:
                    print(f"  TSV files: {tsv_files[:5]}")  # Show first 5

def manual_extraction_guide():
    """Print instructions for manual extraction"""
    print("\n" + "="*60)
    print("MANUAL EXTRACTION GUIDE")
    print("="*60)
    print("""
To extract transcripts from Mozilla Common Voice Delta:

1. Go to the dataset page:
   https://datacollective.mozillafoundation.org/datasets/cmflnuzw62lynu310rvwy9yod

2. Download the dataset (or locate your original download)

3. The dataset includes a 'validated.tsv' or 'test.tsv' file with columns:
   - client_id
   - path (audio filename)
   - sentence (the transcript!)
   - up_votes, down_votes, age, gender, etc.

4. Extract the transcripts:
   - Find the row with path matching your audio file (e.g., 'common_voice_mn_12345.mp3')
   - The 'sentence' column contains the transcript
   
5. Save transcripts to: data/ref/{lang}/{lang}XXXX.txt

Alternatively, if you still have the original download, run:
   python scripts/extract_from_tsv.py --tsv-file path/to/test.tsv --lang mn
""")

def main():
    print("="*60)
    print("MOZILLA COMMON VOICE DELTA TRANSCRIPT EXTRACTION")
    print("="*60)
    
    # Check for original downloads
    extract_from_original_download()
    
    # Print manual guide
    manual_extraction_guide()
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("""
Do you still have the original Common Voice downloads?
If YES:
  1. Find the TSV file (validated.tsv or test.tsv)
  2. Run: python scripts/extract_from_tsv.py --tsv-file path/to/file.tsv --lang mn
  
If NO:
  1. Re-download from: https://datacollective.mozillafoundation.org/datasets/cmflnuzw62lynu310rvwy9yod
  2. Extract the TSV file
  3. Run the TSV extraction script
""")

if __name__ == '__main__':
    main()
