#!/usr/bin/env python3
"""
Profile CPU/GPU/Memory usage for Whisper-medium and Whisper-large-v3
Run this on the GPU server to complete resource profiling for all 6 models
"""

import json
import subprocess
import time
import psutil
import threading
from pathlib import Path
import pandas as pd
import argparse

class ResourceMonitor:
    """Monitor system resources during processing"""
    
    def __init__(self):
        self.measurements = []
        self.monitoring = False
        self.monitor_thread = None
        
    def start(self):
        """Start monitoring"""
        self.monitoring = True
        self.measurements = []
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
    
    def stop(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """Monitoring loop"""
        while self.monitoring:
            measurement = {
                'timestamp': time.time(),
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_used_gb': psutil.virtual_memory().used / (1024**3),
            }
            
            # Try to get GPU stats
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total',
                     '--format=csv,noheader,nounits'],
                    capture_output=True, text=True, timeout=1
                )
                if result.returncode == 0:
                    gpu_stats = result.stdout.strip().split('\n')[0].split(',')
                    measurement['gpu_util'] = float(gpu_stats[0].strip())
                    measurement['gpu_mem_used_mb'] = float(gpu_stats[1].strip())
                    measurement['gpu_mem_total_mb'] = float(gpu_stats[2].strip())
            except:
                measurement['gpu_util'] = 0.0
                measurement['gpu_mem_used_mb'] = 0.0
                measurement['gpu_mem_total_mb'] = 0.0
            
            self.measurements.append(measurement)
            time.sleep(0.5)  # Sample every 0.5 seconds
    
    def get_summary(self):
        """Get summary statistics"""
        if not self.measurements:
            return {
                'cpu_mean': 0, 'cpu_max': 0,
                'memory_mean_gb': 0, 'memory_max_gb': 0,
                'memory_percent_mean': 0, 'memory_percent_max': 0,
                'gpu_util_mean': 0, 'gpu_util_max': 0,
                'gpu_mem_mean_mb': 0, 'gpu_mem_max_mb': 0
            }
        
        df = pd.DataFrame(self.measurements)
        
        summary = {
            'cpu_mean': df['cpu_percent'].mean(),
            'cpu_max': df['cpu_percent'].max(),
            'memory_mean_gb': df['memory_used_gb'].mean(),
            'memory_max_gb': df['memory_used_gb'].max(),
            'memory_percent_mean': df['memory_percent'].mean(),
            'memory_percent_max': df['memory_percent'].max(),
            'gpu_util_mean': df.get('gpu_util', pd.Series([0])).mean(),
            'gpu_util_max': df.get('gpu_util', pd.Series([0])).max(),
            'gpu_mem_mean_mb': df.get('gpu_mem_used_mb', pd.Series([0])).mean(),
            'gpu_mem_max_mb': df.get('gpu_mem_used_mb', pd.Series([0])).max(),
        }
        
        return summary


def profile_whisper(audio_file, model_size, lang, device='cuda'):
    """Profile a single Whisper run"""
    
    print(f"\n  Processing: {audio_file}")
    
    # Start monitoring
    monitor = ResourceMonitor()
    monitor.start()
    
    # Run model
    start_time = time.time()
    
    try:
        cmd = [
            'python', 'scripts/run_whisper.py',
            '--infile', str(audio_file),
            '--mode', 'hinted',
            '--model', model_size,
            '--device', device,
            '--hint-lang', lang,
            '--outdir', '/tmp/profile_test'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0
        if not success:
            print(f"    Error: {result.stderr[:200]}")
        
    except Exception as e:
        print(f"    Exception: {e}")
        success = False
    
    end_time = time.time()
    
    # Stop monitoring
    monitor.stop()
    
    # Get statistics
    elapsed = end_time - start_time
    resource_stats = monitor.get_summary()
    
    print(f"    ✓ {elapsed:.2f}s | CPU: {resource_stats['cpu_mean']:.1f}% | Mem: {resource_stats['memory_max_gb']:.1f}GB | GPU: {resource_stats['gpu_util_mean']:.1f}%")
    
    return {
        'model': model_size,
        'audio_file': str(audio_file),
        'elapsed_sec': elapsed,
        'success': success,
        **resource_stats
    }


def main():
    parser = argparse.ArgumentParser(description='Profile Whisper medium and large-v3')
    parser.add_argument('--samples', type=int, default=10,
                        help='Number of samples per language')
    parser.add_argument('--device', default='cuda',
                        help='Device to use (cuda or cpu)')
    parser.add_argument('--output', default='results/resource_profiling_whisper_extended.csv',
                        help='Output CSV file')
    
    args = parser.parse_args()
    
    print("="*60)
    print("WHISPER MEDIUM & LARGE-V3 RESOURCE PROFILING")
    print("="*60)
    print(f"Samples per language: {args.samples}")
    print(f"Device: {args.device}")
    print(f"Output: {args.output}")
    
    # Languages and models
    langs = ['mn', 'hu', 'es', 'fr']
    models = ['medium', 'large-v3']
    
    results = []
    
    for model in models:
        print(f"\n{'='*60}")
        print(f"MODEL: Whisper-{model}")
        print(f"{'='*60}")
        
        for lang in langs:
            print(f"\n--- Language: {lang.upper()} ---")
            
            # Get sample files
            audio_dir = Path(f'data/wav/{lang}')
            if not audio_dir.exists():
                print(f"  Warning: {audio_dir} not found, skipping")
                continue
                
            audio_files = sorted(audio_dir.glob('*.mp3'))[:args.samples]
            
            if not audio_files:
                print(f"  Warning: No audio files found in {audio_dir}")
                continue
            
            for audio_file in audio_files:
                result = profile_whisper(audio_file, model, lang, args.device)
                results.append(result)
    
    # Save results
    df = pd.DataFrame(results)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    
    print(f"\n{'='*60}")
    print("✅ PROFILING COMPLETE")
    print(f"{'='*60}")
    print(f"Results saved to: {args.output}")
    print(f"Total runs: {len(results)}")
    
    # Print summary
    print(f"\n--- SUMMARY ---")
    for model in models:
        model_df = df[df['model'] == model]
        if len(model_df) > 0:
            print(f"\nWhisper-{model}:")
            print(f"  CPU Avg: {model_df['cpu_mean'].mean():.1f}%")
            print(f"  CPU Peak: {model_df['cpu_max'].max():.1f}%")
            print(f"  Memory Peak: {model_df['memory_max_gb'].max():.2f} GB")
            print(f"  GPU Avg: {model_df['gpu_util_mean'].mean():.1f}%")
            print(f"  Avg Time: {model_df['elapsed_sec'].mean():.2f}s")


if __name__ == '__main__':
    main()
