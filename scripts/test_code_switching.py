#!/usr/bin/env python3
"""
Simple code-switching test as advised by supervisor.
Concatenates audio from different languages and tests ASR behavior.
"""

import os
import json
from pydub import AudioSegment
import whisper
import time

def concatenate_audio(audio_files, output_path):
    """Concatenate multiple audio files"""
    combined = AudioSegment.empty()
    
    for audio_file in audio_files:
        audio = AudioSegment.from_mp3(audio_file)
        combined += audio
    
    combined.export(output_path, format="mp3")
    print(f"✓ Created concatenated audio: {output_path}")
    print(f"  Total duration: {len(combined)/1000:.2f}s")
    return len(combined)/1000

def test_code_switching(model_name="small"):
    """Test Whisper's behavior on code-switched audio"""
    
    print("="*70)
    print("CODE-SWITCHING EXPERIMENT")
    print("="*70)
    print()
    print("Testing if Whisper detects language switches in concatenated audio")
    print()
    
    # Load model
    print(f"Loading Whisper {model_name}...")
    model = whisper.load_model(model_name)
    
    # Create test cases: concatenate audio from different languages
    test_cases = [
        {
            'name': 'Spanish-Mongolian',
            'files': [
                'data/wav/es/es0001.mp3',
                'data/wav/mn/mn0001.mp3'
            ],
            'expected': ['es', 'mn']
        },
        {
            'name': 'French-Hungarian-Spanish',
            'files': [
                'data/wav/fr/fr0001.mp3',
                'data/wav/hu/hu0001.mp3',
                'data/wav/es/es0001.mp3'
            ],
            'expected': ['fr', 'hu', 'es']
        },
        {
            'name': 'Mongolian-Spanish-French',
            'files': [
                'data/wav/mn/mn0001.mp3',
                'data/wav/es/es0001.mp3',
                'data/wav/fr/fr0001.mp3'
            ],
            'expected': ['mn', 'es', 'fr']
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 70)
        
        # Create concatenated audio
        output_path = f"data/code_switching_test_{i}.mp3"
        
        # Check if files exist
        existing_files = [f for f in test_case['files'] if os.path.exists(f)]
        if len(existing_files) != len(test_case['files']):
            print(f"⚠️  Skipping - not all audio files found")
            continue
        
        duration = concatenate_audio(existing_files, output_path)
        
        # Transcribe with LID
        print("Running transcription with LID enabled...")
        start_time = time.time()
        
        result = model.transcribe(
            output_path,
            language=None,  # Enable LID
            task='transcribe',
            verbose=False
        )
        
        elapsed = time.time() - start_time
        
        # Extract detected language
        detected_lang = result.get('language', 'unknown')
        
        print(f"  Detected language: {detected_lang}")
        print(f"  Expected languages: {', '.join(test_case['expected'])}")
        print(f"  Processing time: {elapsed:.2f}s")
        print(f"  Transcription: {result['text'][:100]}...")
        
        # Check if it detected language switches (segments)
        if 'segments' in result:
            segment_langs = []
            for seg in result['segments'][:5]:  # First 5 segments
                # Whisper doesn't provide per-segment language in standard output
                # We can only check if it stays consistent or switches
                segment_langs.append(seg.get('text', '')[:50])
            
            print(f"  First segments: {len(result['segments'])} total")
        
        results.append({
            'test_name': test_case['name'],
            'expected_languages': test_case['expected'],
            'detected_language': detected_lang,
            'duration_sec': duration,
            'processing_time_sec': elapsed,
            'transcription': result['text'],
            'num_segments': len(result.get('segments', []))
        })
        
        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)
    
    # Save results
    output_file = 'results/code_switching_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print()
    print("="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    for result in results:
        print(f"\n{result['test_name']}:")
        print(f"  Expected: {' → '.join(result['expected_languages'])}")
        print(f"  Detected: {result['detected_language']}")
        print(f"  Behavior: ", end="")
        
        if result['detected_language'] == result['expected_languages'][0]:
            print("✓ Locked to first language (no switch detected)")
        elif result['detected_language'] in result['expected_languages']:
            print(f"⚠️  Detected {result['detected_language']} (partial)")
        else:
            print(f"✗ Unexpected language: {result['detected_language']}")
    
    print()
    print(f"✓ Results saved to: {output_file}")
    print()
    print("="*70)
    print("INTERPRETATION:")
    print("="*70)
    print("If Whisper locks to the first language:")
    print("  → LID happens once at the start, no intra-utterance switching")
    print()
    print("If it detects mixed languages:")
    print("  → Model attempts to handle code-switching")
    print()
    print("This simple test reveals whether current architecture can")
    print("handle code-switching or requires external segmentation.")
    print("="*70)

if __name__ == '__main__':
    test_code_switching()
