#!/usr/bin/env python3
"""
Download Common Voice audio samples for Spanish and French
Run this on Saturday when you have fast internet!
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys

def download_language_samples(lang_code, num_samples=1000, output_dir="data/wav"):
    """
    Download Common Voice samples for a language
    
    Args:
        lang_code: Language code (es, fr)
        num_samples: Number of samples to download
        output_dir: Output directory
    """
    print(f"\n{'='*60}")
    print(f"Downloading {num_samples} samples for {lang_code.upper()}")
    print(f"{'='*60}\n")
    
    # Create output directory
    lang_dir = Path(output_dir) / lang_code
    lang_dir.mkdir(parents=True, exist_ok=True)
    
    # Instructions for manual download
    print(f"""
📥 DOWNLOAD INSTRUCTIONS:

1. Go to: https://commonvoice.mozilla.org/en/datasets
2. Select language: {lang_code.upper()}
3. Download the dataset (requires Mozilla account)
4. Extract the .tar.gz file
5. Navigate to the 'clips' folder
6. Copy {num_samples} .mp3 files to: {lang_dir.absolute()}

NAMING CONVENTION:
- Rename files to: {lang_code}0001.mp3, {lang_code}0002.mp3, etc.
- Or use the batch rename script below

BATCH RENAME COMMAND (run in clips folder):
    ls -1 *.mp3 | head -{num_samples} | awk '{{printf "mv %s {lang_code}%04d.mp3\\n", $0, NR}}' | bash

Press Enter when files are ready in {lang_dir.absolute()}
""")
    
    input("Press Enter to continue...")
    
    # Verify files
    mp3_files = list(lang_dir.glob("*.mp3"))
    print(f"\n✅ Found {len(mp3_files)} files in {lang_dir}")
    
    if len(mp3_files) < num_samples:
        print(f"⚠️  WARNING: Expected {num_samples} files but found {len(mp3_files)}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    return len(mp3_files)

def main():
    parser = argparse.ArgumentParser(description="Download Common Voice samples")
    parser.add_argument("--langs", nargs="+", default=["es", "fr"],
                       help="Language codes to download")
    parser.add_argument("--num-samples", type=int, default=1000,
                       help="Number of samples per language")
    parser.add_argument("--output-dir", default="data/wav",
                       help="Output directory")
    
    args = parser.parse_args()
    
    print(f"""
🌍 Common Voice Batch Download
{'='*60}
Languages: {', '.join(args.langs)}
Samples per language: {args.num_samples}
Output directory: {args.output_dir}
{'='*60}
""")
    
    total_downloaded = 0
    for lang in args.langs:
        count = download_language_samples(lang, args.num_samples, args.output_dir)
        total_downloaded += count
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE: {total_downloaded} total files ready!")
    print(f"{'='*60}\n")
    
    # Next steps
    print("""
📤 NEXT STEPS:

1. Create archive for upload:
   tar -czf cv_es_fr.tar.gz data/wav/es data/wav/fr

2. Upload to GPU server:
   scp -P 15270 cv_es_fr.tar.gz mugi@bistromat.tmit.bme.hu:~/

3. On server, extract:
   ssh -p 15270 mugi@bistromat.tmit.bme.hu
   tar -xzf cv_es_fr.tar.gz

4. Run experiment:
   nohup ./scripts/run_comparison_batch.sh small cpu > experiment_es_fr.txt 2>&1 &
""")

if __name__ == "__main__":
    main()
