#!/usr/bin/env python3
"""
Profile CPU/GPU/Memory usage during ASR processing
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
                    measurement['gpu_util'] = float(gpu_stats[0])
                    measurement['gpu_mem_used_mb'] = float(gpu_stats[1])
                    measurement['gpu_mem_total_mb'] = float(gpu_stats[2])
            except:
                pass
            
            self.measurements.append(measurement)
            time.sleep(1.0)  # Sample every second
    
    def get_summary(self):
        """Get summary statistics"""
        if not self.measurements:
            return {}
        
        df = pd.DataFrame(self.measurements)
        
        summary = {
            'cpu_mean': df['cpu_percent'].mean(),
            'cpu_max': df['cpu_percent'].max(),
            'memory_mean_gb': df['memory_used_gb'].mean(),
            'memory_max_gb': df['memory_used_gb'].max(),
            'memory_percent_mean': df['memory_percent'].mean(),
            'memory_percent_max': df['memory_percent'].max(),
        }
        
        if 'gpu_util' in df.columns:
            summary.update({
                'gpu_util_mean': df['gpu_util'].mean(),
                'gpu_util_max': df['gpu_util'].max(),
                'gpu_mem_mean_mb': df['gpu_mem_used_mb'].mean(),
                'gpu_mem_max_mb': df['gpu_mem_used_mb'].max(),
            })
        
        return summary

def profile_model(model_script, audio_file, output_file, **kwargs):
    """Profile a single model run"""
    
    print(f"\nProfiling: {model_script}")
    print(f"Audio: {audio_file}")
    
    # Start monitoring
    monitor = ResourceMonitor()
    monitor.start()
    
    # Run model
    start_time = time.time()
    
    try:
        # Build command based on model type
        if 'whisper' in model_script:
            cmd = [
                'python', model_script,
                '--infile', audio_file,
                '--mode', kwargs.get('mode', 'hinted'),
                '--model', kwargs.get('model', 'small'),
                '--device', kwargs.get('device', 'cpu'),
                '--outdir', '/tmp/profile_test'
            ]
            if kwargs.get('hint_lang'):
                cmd.extend(['--hint-lang', kwargs['hint_lang']])
        else:  # omnilingual
            cmd = [
                'python', model_script,
                '--infile', audio_file,
                '--hint-lang', kwargs.get('hint_lang', 'es'),
                '--model', kwargs.get('model', 'omniASR_CTC_300M'),
                '--outdir', '/tmp/profile_test'
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = result.returncode == 0
        
    except Exception as e:
        print(f"Error: {e}")
        success = False
    
    end_time = time.time()
    
    # Stop monitoring
    monitor.stop()
    
    # Get statistics
    elapsed = end_time - start_time
    resource_stats = monitor.get_summary()
    
    # Combine results
    profile_data = {
        'model': kwargs.get('model', 'unknown'),
        'audio_file': audio_file,
        'elapsed_sec': elapsed,
        'success': success,
        **resource_stats
    }
    
    # Save
    df = pd.DataFrame([profile_data])
    if Path(output_file).exists():
        df_existing = pd.read_csv(output_file)
        df = pd.concat([df_existing, df], ignore_index=True)
    
    df.to_csv(output_file, index=False)
    
    print(f"✓ Profiled in {elapsed:.2f}s")
    print(f"  CPU: {resource_stats.get('cpu_mean', 0):.1f}% (max {resource_stats.get('cpu_max', 0):.1f}%)")
    print(f"  Memory: {resource_stats.get('memory_mean_gb', 0):.2f} GB (max {resource_stats.get('memory_max_gb', 0):.2f} GB)")
    if 'gpu_util_mean' in resource_stats:
        print(f"  GPU: {resource_stats['gpu_util_mean']:.1f}% (max {resource_stats['gpu_util_max']:.1f}%)")
        print(f"  GPU Mem: {resource_stats['gpu_mem_mean_mb']:.0f} MB (max {resource_stats['gpu_mem_max_mb']:.0f} MB)")
    
    return profile_data

def main():
    parser = argparse.ArgumentParser(description='Profile resource usage')
    parser.add_argument('--samples-per-lang', type=int, default=10,
                        help='Number of samples to profile per language/model')
    parser.add_argument('--output', default='results/resource_profiling.csv',
                        help='Output CSV file')
    
    args = parser.parse_args()
    
    print("="*60)
    print("RESOURCE USAGE PROFILING")
    print("="*60)
    
    # Sample files from each language
    langs = ['mn', 'hu', 'es', 'fr']
    models_to_test = [
        ('scripts/run_whisper.py', {'model': 'small', 'mode': 'hinted'}),
        ('scripts/run_omnilingual.py', {'model': 'omniASR_CTC_300M'}),
        ('scripts/run_omnilingual.py', {'model': 'omniASR_CTC_1B'}),
        ('scripts/run_omnilingual.py', {'model': 'omniASR_LLM_1B'}),
    ]
    
    for lang in langs:
        audio_files = list(Path(f'data/wav/{lang}').glob('*.mp3'))[:args.samples_per_lang]
        
        for audio_file in audio_files:
            for model_script, model_params in models_to_test:
                profile_model(
                    model_script,
                    str(audio_file),
                    args.output,
                    hint_lang=lang,
                    **model_params
                )
    
    print("\n" + "="*60)
    print("✅ PROFILING COMPLETE")
    print("="*60)
    print(f"Results saved to: {args.output}")

if __name__ == '__main__':
    main()
