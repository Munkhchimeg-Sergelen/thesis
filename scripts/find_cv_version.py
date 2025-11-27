#!/usr/bin/env python3
"""
Find working Common Voice dataset versions
"""

from datasets import load_dataset_builder
from huggingface_hub import list_datasets

print("Searching for Common Voice datasets...")
print("="*60)

# Search for Common Voice datasets
datasets = list(list_datasets(search="common_voice", author="mozilla-foundation"))

print(f"\nFound {len(datasets)} Common Voice datasets:\n")

for ds in datasets[:20]:  # Show first 20
    print(f"  - {ds.id}")
    
print("\n" + "="*60)
print("\nTrying to load Common Voice 17.0 (latest)...")

# Try the new format
try:
    # Common Voice 17.0 uses a different structure
    ds = load_dataset_builder("mozilla-foundation/common_voice_17_0", "mn")
    print(f"✓ Found Common Voice 17.0!")
    print(f"  Available configs: {ds.BUILDER_CONFIGS}")
except Exception as e:
    print(f"  Failed: {e}")

print("\nTrying streaming mode...")
try:
    from datasets import load_dataset
    ds = load_dataset("mozilla-foundation/common_voice_17_0", "mn", split="test", streaming=True)
    sample = next(iter(ds))
    print("✓ Streaming works!")
    print(f"  Sample keys: {list(sample.keys())}")
    if 'sentence' in sample:
        print(f"  Sample text: {sample['sentence'][:50]}...")
except Exception as e:
    print(f"  Failed: {e}")
