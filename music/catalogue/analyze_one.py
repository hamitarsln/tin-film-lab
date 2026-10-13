import json, sys
from pathlib import Path
from analyze import analyze
p = Path(sys.argv[1]); out = p.parent.parent / "analysis" / (p.stem + ".json")
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(analyze(str(p))))
