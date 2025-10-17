import sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from framing.config import cfg
from framing.preprocessing import preprocess_one

if __name__ == "__main__":
    print(f"Index:     {cfg.index_path}")
    print(f"Processed: {cfg.data_processed_dir}")

    entries = json.loads(cfg.index_path.read_text(encoding="utf-8"))
    written = []

    for i, row in enumerate(entries, 1):
        src = ROOT / Path(row["source_path"])
        if not src.exists():
            print(f"⚠️  [{i}] Datei fehlt: {src}")
            continue
        item = preprocess_one(src, text_id=row["id"], label=row.get("label",""))
        if len(item.get("tokens", [])) < 5:  # ggf. cfg.min_tokens nutzen
            print(f"⚠️  [{i}] Zu wenig Tokens, skip: id={row['id']}")
            continue
        out_path = cfg.data_processed_dir / f"{item['id']}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ [{i}] {row['id']} → {out_path.name}")
        written.append(out_path)

    if not written:
        print("Keine Dateien geschrieben.")
    else:
        print(f"🎯 Done. {len(written)} Datei(en).")
