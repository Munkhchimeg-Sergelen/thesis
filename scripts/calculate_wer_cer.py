#!/usr/bin/env python3
"""
Calculate WER (Word Error Rate) and CER (Character Error Rate)
for ASR model outputs against reference transcripts
"""

import json
import argparse
from pathlib import Path
import pandas as pd
import jiwer

def load_reference_files(ref_dir, lang):
    """Load reference transcripts from individual .txt files"""
    references = {}
    ref_path = Path(ref_dir) / lang
    
    if not ref_path.exists():
        print(f"    ⚠️  Reference directory not found: {ref_path}")
        return references
    
    # Load individual .txt files (e.g., mn0001.txt, mn0002.txt)
    txt_files = list(ref_path.glob(f"{lang}*.txt"))
    
    for txt_file in txt_files:
        file_id = txt_file.stem  # e.g., 'mn0001'
        with open(txt_file, 'r', encoding='utf-8') as f:
            transcript = f.read().strip()
            if transcript:
                references[file_id] = transcript
    
    return references

def calculate_metrics(hypothesis, reference):
    """Calculate WER and CER for a single pair"""
    # Normalize
    hyp = hypothesis.strip()
    ref = reference.strip()
    
    if not ref:
        return None, None
    
    # WER
    try:
        wer = jiwer.wer(ref, hyp)
    except:
        wer = None
    
    # CER  
    try:
        cer = jiwer.cer(ref, hyp)
    except:
        cer = None
    
    return wer, cer

def process_model_language(model_dir, ref_data, lang):
    """Process all files for one model/language"""
    results = []
    
    json_files = list(model_dir.glob("*.json"))
    
    for json_file in json_files:
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            file_id = Path(data.get('file', '')).stem
            
            # Get hypothesis - check JSON first, then .txt file
            hypothesis = data.get('transcript', '')
            
            if not hypothesis:
                # Whisper saves transcripts as separate .txt files
                txt_file = json_file.with_suffix('.txt')
                if txt_file.exists():
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        hypothesis = f.read().strip()
            
            if not hypothesis:
                print(f"⚠️  No transcript for {file_id}")
                continue
            
            # Get reference
            if isinstance(ref_data, dict):
                reference = ref_data.get(file_id, ref_data.get(file_id.replace(f'{lang}', ''), ''))
            else:
                reference = ref_data  # Single reference for all
            
            if not reference:
                print(f"⚠️  No reference for {file_id}")
                continue
            
            wer, cer = calculate_metrics(hypothesis, reference)
            
            if wer is not None:
                results.append({
                    'file_id': file_id,
                    'wer': wer,
                    'cer': cer,
                    'hypothesis': hypothesis,
                    'reference': reference
                })
        
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Calculate WER and CER')
    parser.add_argument('--results-dir', default='results/transcripts/hinted',
                      help='Base results directory')
    parser.add_argument('--ref-dir', default='data/ref',
                      help='Reference transcripts directory')
    parser.add_argument('--languages', nargs='+', default=['mn', 'hu', 'es', 'fr'],
                      help='Languages to process')
    parser.add_argument('--output', default='results/wer_cer_results.csv',
                      help='Output CSV file')
    
    args = parser.parse_args()
    
    results_base = Path(args.results_dir)
    ref_base = Path(args.ref_dir)
    
    all_results = []
    
    print("="*60)
    print("WER/CER CALCULATION")
    print("="*60)
    
    # Models to process
    models = {
        'Whisper-small': ('whisper-small', ''),
        'omniASR_CTC_300M': ('omnilingual', 'omniASR_CTC_300M'),
        'omniASR_CTC_1B': ('omnilingual', 'omniASR_CTC_1B'),
        'omniASR_LLM_1B': ('omnilingual', 'omniASR_LLM_1B'),
    }
    
    for model_name, (system, model_subdir) in models.items():
        print(f"\n{'='*60}")
        print(f"Processing: {model_name}")
        print(f"{'='*60}")
        
        for lang in args.languages:
            print(f"\n  Language: {lang.upper()}")
            
            # Load references from individual files
            ref_data = load_reference_files(ref_base, lang)
            if not ref_data:
                print(f"    ⚠️  No reference files found")
                continue
            
            print(f"    ✓ Loaded {len(ref_data)} references")
            
            # Find model directory
            if model_subdir:
                model_dir = results_base / system / model_subdir / lang
            else:
                model_dir = results_base / system / lang
            
            if not model_dir.exists():
                print(f"    ⚠️  Model directory not found: {model_dir}")
                continue
            
            # Process files
            lang_results = process_model_language(model_dir, ref_data, lang)
            
            if lang_results:
                # Calculate averages
                df_lang = pd.DataFrame(lang_results)
                avg_wer = df_lang['wer'].mean()
                avg_cer = df_lang['cer'].mean()
                
                print(f"    ✓ Processed {len(lang_results)} files")
                print(f"    WER: {avg_wer:.2%}  CER: {avg_cer:.2%}")
                
                # Add to overall results
                for result in lang_results:
                    result['model'] = model_name
                    result['language'] = lang
                    all_results.append(result)
    
    if not all_results:
        print("\n❌ No results calculated!")
        return
    
    # Save detailed results
    df_all = pd.DataFrame(all_results)
    df_all.to_csv(args.output, index=False)
    print(f"\n✓ Saved detailed results: {args.output}")
    
    # Calculate and save summary statistics
    summary = df_all.groupby(['model', 'language']).agg({
        'wer': ['mean', 'std', 'min', 'max'],
        'cer': ['mean', 'std', 'min', 'max']
    }).round(4)
    
    summary_file = args.output.replace('.csv', '_summary.csv')
    summary.to_csv(summary_file)
    print(f"✓ Saved summary: {summary_file}")
    
    # Print summary table
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print("\n" + summary.to_string())
    
    print("\n" + "="*60)
    print("✅ WER/CER Calculation Complete!")
    print("="*60)

if __name__ == '__main__':
    main()
