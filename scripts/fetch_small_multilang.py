from datasets import load_dataset
import soundfile as sf, os, re

# FLEURS locales (valid)
FLEURS = {"mn":"mn_mn", "hu":"hu_hu", "fr":"fr_fr", "es":"es_419"}

def slug(s):
    s = "" if s is None else str(s)
    return re.sub(r'[^a-zA-Z0-9_-]+','_', s.strip())[:40] or "utt"

def ensure_dirs(lang):
    os.makedirs(f"data/wav/{lang}", exist_ok=True)
    os.makedirs(f"data/ref/{lang}", exist_ok=True)

def write_pair(lang, base, arr, sr, text):
    sf.write(f"data/wav/{lang}/{base}.wav", arr, sr)
    with open(f"data/ref/{lang}/{base}.txt","w",encoding="utf-8") as f:
        f.write("" if text is None else str(text))

def try_fleurs(lang, k=10):
    loc = FLEURS[lang]
    ds = load_dataset("google/fleurs", loc, split="test",
                      streaming=True, trust_remote_code=True)
    i = 0
    for ex in ds:
        base = f"{lang}{i+1:02d}_{slug(ex.get('id','fleurs'))}"
        arr = ex["audio"]["array"]; sr = ex["audio"]["sampling_rate"]
        txt = ex.get("transcription") or ex.get("raw_transcription") or ""
        write_pair(lang, base, arr, sr, txt)
        i += 1
        if i >= k: break
    return i

def main():
    any_ok = False
    for lang in ["mn","hu","fr","es"]:
        ensure_dirs(lang)
        print(f"==> {lang}: FLEURS (streaming)")
        try:
            n = try_fleurs(lang, k=10)
            print(f"   {lang}: grabbed {n} clips")
            any_ok |= (n > 0)
        except Exception as e:
            print(f"   {lang}: FLEURS failed: {e}")
    if not any_ok:
        raise SystemExit("No data fetched. Check Internet.")
    print("Done.")
if __name__ == "__main__":
    main()
