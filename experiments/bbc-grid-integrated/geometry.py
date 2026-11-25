from pathlib import Path
import json

out = Path("out")
names = ("paper in her kitchen", "Amner Hall", "Huang and Trump", "returns to the office")
url = "https://www.bbc.co.uk/news"

def native(path):
    data = json.loads(path.read_text())
    assert data["url"] == url
    cards = {}
    for card in data["cards"]:
        matches = []
        for instance in card["instances"]:
            chain = instance["chain"]
            for x, y, w, h in chain[0]["boxes"]:
                if 0 <= y < 300 and w > 100 and h > 50:
                    matches.append([x, y, w, h])
        assert len(matches) == 1, (path, card["needle"], matches)
        cards[card["needle"]] = matches[0]
    return cards

base = native(out / "baseline/foafnaut-geometry.json")
patched = native(out / "candidate/foafnaut-geometry.json")
browser = json.loads(Path("reference/chrome.json").read_text())
assert browser["url"] == url and browser["viewport"] == [1280, 735]
chrome = {}
for card in browser["boxes"]:
    if card["needle"] in names and card["decoded"][0] > 0:
        box = card["chain"][0]["box"]
        if 0 <= box[1] < 300 and box[2] > 100 and box[3] > 50:
            assert card["needle"] not in chrome, card
            chrome[card["needle"]] = box

results = {name: {"baseline": base[name], "candidate": patched[name], "chrome": chrome[name]} for name in names}
(out / "comparison.json").write_text(json.dumps(results, indent=2) + "\n")
print("| Photo | Baseline height | Integrated height | Chrome height |")
print("| --- | ---: | ---: | ---: |")
for name, row in results.items():
    print(f"| {name} | {row['baseline'][3]:.3f} | {row['candidate'][3]:.3f} | {row['chrome'][3]:.3f} |")
for name, row in results.items():
    _, _, width, height = row["candidate"]
    expected = row["chrome"][3]
    previous = row["baseline"][3]
    assert abs(height - width * 9 / 16) <= 1, (name, row, "16:9 aspect ratio")
    assert abs(height - expected) <= 5, (name, row, "Chrome comparison")
    assert abs(height - expected) < abs(previous - expected), (name, row, "improvement")
