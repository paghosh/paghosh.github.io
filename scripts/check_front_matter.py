#!/usr/bin/env python3
"""Fail if any page's YAML front matter does not parse (a colon in an unquoted description is the usual cause)."""
import glob, sys, yaml
bad = 0
for f in glob.glob("*.html") + glob.glob("*.md") + glob.glob("**/*.xml", recursive=True) + glob.glob("research/*.bib*"):
    s = open(f).read()
    if not s.startswith("---"):
        continue
    try:
        fm = yaml.safe_load(s.split("---", 2)[1])
        if f.endswith((".html", ".md")) and not fm.get("title") and not fm.get("layout") == "null" and f != "index.html":
            print("no title:", f); bad += 1
    except Exception as e:
        print("BAD front matter:", f, e); bad += 1
for f in glob.glob("_data/*.yml"):
    try: yaml.safe_load(open(f))
    except Exception as e: print("BAD data:", f, e); bad += 1
print("front matter check:", "FAILED" if bad else "ok")
sys.exit(1 if bad else 0)
