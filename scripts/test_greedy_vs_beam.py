#!/usr/bin/env python3
"""
Test greedy decoding vs beam search for Mongolian performance
Compare processing times with beam_size=1 (greedy) vs beam_size=5 (default)
"""

import time
import json
from pathlib import Path
from faster_whisper import WhisperModel

# Test files - pick a few from each language
TEST_FILES = {
    'mn': ['data/wav/mn/mn0001.mp3', 'data/wav/mn/mn0002.mp3', 'data/wav/mn/mn0003.mp3'],
    'hu': ['data/wav/hu/hu0001.mp3', 'data/wav/hu/hu0002.mp3', 'data/wav/hu/hu0003.mp3'],
    'es': ['data/wav/es/es0001.mp3', 'data/wav/es/es0002.mp3', 'data/wav/es/es0003.mp3'],
    'fr': ['data/wav/fr/fr0001.mp3', 'data/wav/fr/fr0002.mp3', 'data/wav/fr/fr0003.mp3'],
}

BEAM_SIZES = [1, 5]  # 1=greedy, 5=beam search

print("=" * 70)
print("TESTING GREEDY vs BEAM SEARCH DECODING")
print("=" * 70)
print()

# Load model once
model = WhisperModel("small", device="cpu")

results = []

for beam_size in BEAM_SIZES:
    print(f"\n{'='*70}")
    print(f"BEAM SIZE: {beam_size} ({'GREEDY' if beam_size == 1 else 'BEAM SEARCH'})")
    print(f"{'='*70}\n")
    
    for lang, files in TEST_FILES.items():
        print(f"\n{lang.upper()}:")
        lang_times = []
        
        for audio_file in files:
            if not Path(audio_file).exists():
                print(f"  ⚠️  {audio_file} not found, skipping")
                continue
                
            t0 = time.time()
            segments, info = model.transcribe(
                audio_file,
                task="transcribe",
                language=lang,
                vad_filter=True,
                beam_size=beam_size  # KEY PARAMETER
            )
            # Force evaluation
            text = "".join(s.text for s in segments)
            elapsed = time.time() - t0
            
            duration = getattr(info, 'duration', None)
            rtf = elapsed / duration if duration else None
            
            lang_times.append(elapsed)
            
            print(f"  {Path(audio_file).name}: {elapsed:.3f}s (RTF: {rtf:.3f})")
            
            results.append({
                'language': lang,
                'file': audio_file,
                'beam_size': beam_size,
                'elapsed_sec': elapsed,
                'duration_sec': duration,
                'rtf': rtf
            })
        
        if lang_times:
            avg_time = sum(lang_times) / len(lang_times)
            print(f"  → Average: {avg_time:.3f}s")

print("\n" + "="*70)
print("SUMMARY COMPARISON")
print("="*70)

# Compare averages by language and beam size
for lang in TEST_FILES.keys():
    lang_results = [r for r in results if r['language'] == lang]
    
    greedy_times = [r['elapsed_sec'] for r in lang_results if r['beam_size'] == 1]
    beam_times = [r['elapsed_sec'] for r in lang_results if r['beam_size'] == 5]
    
    if greedy_times and beam_times:
        greedy_avg = sum(greedy_times) / len(greedy_times)
        beam_avg = sum(beam_times) / len(beam_times)
        speedup = beam_avg / greedy_avg
        
        print(f"\n{lang.upper()}:")
        print(f"  Greedy (beam=1):     {greedy_avg:.3f}s")
        print(f"  Beam Search (beam=5): {beam_avg:.3f}s")
        print(f"  Speedup with greedy:  {speedup:.2f}x")

# Save detailed results
output_file = "results/analysis/greedy_vs_beam_test.json"
Path(output_file).parent.mkdir(parents=True, exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Detailed results saved to: {output_file}")
print("\nConclusion: If Mongolian shows large speedup with greedy,")
print("then beam search is the bottleneck!")
