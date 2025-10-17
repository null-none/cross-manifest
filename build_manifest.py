import json, shutil
from pathlib import Path
from copy import deepcopy

EXT_DIR = Path("extension")
base_path = Path("manifest.base.json")
base = json.loads(base_path.read_text(encoding="utf-8"))

def make_firefox(m):
    m = deepcopy(m)
    m["manifest_version"] = 2
    if "action" in m:
        m["browser_action"] = m.pop("action")
    bg = m.get("background", {})
    if "service_worker" in bg:
        bg["scripts"] = [bg.pop("service_worker")]
        bg["persistent"] = False
    m["background"] = bg
    return m

def make_mv3(m):
    m = deepcopy(m)
    m["manifest_version"] = 3
    if "browser_action" in m:
        m["action"] = m.pop("browser_action")
    bg = m.get("background", {})
    if "scripts" in bg:
        bg["service_worker"] = bg["scripts"][0]
        bg.pop("scripts", None)
        bg.pop("persistent", None)
    m["background"] = bg
    return m

def copy_content(browser):
    out_dir = Path(f"dist/{browser}")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(EXT_DIR, out_dir)

def save_manifest(browser, data):
    out_path = Path(f"dist/{browser}/manifest.json")
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ {browser}: {out_path}")

def build(browser, transform):
    copy_content(browser)
    save_manifest(browser, transform(base))

build("firefox", make_firefox)
for b in ["chrome", "edge", "opera"]:
    build(b, make_mv3)
