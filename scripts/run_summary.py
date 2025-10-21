#!/usr/bin/env python3
import argparse, os, json, csv, glob
import soundfile as sf

LANGS = {"mn","hu","fr","es"}

def infer_lang_from_path(p):
    parts = p.replace("\\","/").split("/")
    for part in parts:
        if part in LANGS: return part
    return "unk"

def load_lid_map(lid_dir):
    lid = {}
    for fp in glob.glob(os.path.join(lid_dir, "*.json")):
        j = json.load(open(fp, encoding="utf-8"))
        lid[j["file"]] = {
            "lid_pred": j.get("pred_lang"),
            "lid_conf": j.get("confidence"),
        }
    return lid

def audio_duration_sec(wav_path):
    try:
        info = sf.info(wav_path)
        return float(info.frames)/float(info.samplerate)
    except Exception:
        return None

def iter_asr_sidecars(root_dir):
    # expects .../transcripts/<mode>/<system>/<lang>/json/*.json
    for fp in glob.glob(os.path.join(root_dir, "*", "*", "*", "json", "*.json")):
        parts = fp.replace("\\","/").split("/")
        # ... transcripts/<mode>/<system>/<lang>/json/file.json
        try:
            idx = parts.index("transcripts")
        except ValueError:
            continue
        mode  = parts[idx+1] if idx+1 < len(parts) else "unk"
        system= parts[idx+2] if idx+2 < len(parts) else "unk"
        lang  = parts[idx+3] if idx+3 < len(parts) else "unk"
        j = json.load(open(fp, encoding="utf-8"))
        yield fp, mode, system, lang, j

def load_manifest_buckets(manifest_dir):
    # map absolute path -> bucket
    buckets = {}
    for mf in glob.glob(os.path.join(manifest_dir, "*.csv")):
        with open(mf, encoding="utf-8") as f:
            next(f, None)  # header
            for line in f:
                line=line.strip()
                if not line: continue
                file_path, lang, dur, buck = line.split(",", 3)
                buckets[file_path] = buck
    return buckets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcripts-root", default="results/transcripts")
    ap.add_argument("--lid-dir", default="results/logs/lid")
    ap.add_argument("--manifest-dir", default="results/manifests")
    ap.add_argument("--out", default="results/metrics/run_summary.csv")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    lid_map = load_lid_map(args.lid_dir) if os.path.isdir(args.lid_dir) else {}
    buckets = load_manifest_buckets(args.manifest_dir) if os.path.isdir(args.manifest_dir) else {}

    rows = []
    for sidecar_fp, mode, system, path_lang, side in iter_asr_sidecars(args.transcripts_root):
        wav_path     = side.get("file")
        ref_lang     = infer_lang_from_path(wav_path) if wav_path else "unk"
        lid_pred     = lid_map.get(wav_path,{}).get("lid_pred")
        lid_conf     = lid_map.get(wav_path,{}).get("lid_conf")
        latency_sec  = side.get("latency_sec")
        dur_sec      = audio_duration_sec(wav_path) if wav_path else None
        rtf          = (dur_sec/latency_sec) if (dur_sec and latency_sec and latency_sec>0) else None
        avg_logprob  = side.get("avg_logprob")
        no_speech    = side.get("no_speech_prob")
        bucket       = buckets.get(wav_path)
        text_len     = None
        # extract transcript length (characters) from adjacent txt if available
        base = os.path.splitext(os.path.basename(sidecar_fp))[0]
        txt_fp = sidecar_fp.replace("/json/", "/txt/").rsplit(".", 1)[0] + ".txt"
        if os.path.exists(txt_fp):
            try:
                with open(txt_fp, encoding="utf-8") as f:
                    text_len = len(f.read().strip())
            except Exception:
                pass

        rows.append([
            wav_path, ref_lang, mode, system, path_lang,
            lid_pred, lid_conf, latency_sec, dur_sec, rtf,
            avg_logprob, no_speech, bucket, text_len
        ])

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "file","ref_lang","mode","system","path_lang",
            "lid_pred","lid_conf","latency_sec","audio_sec","rtf",
            "avg_logprob","no_speech_prob","bucket","text_len"
        ])
        w.writerows(rows)
    print("run summary →", args.out, f"({len(rows)} rows)")
if __name__ == "__main__":
    main()
