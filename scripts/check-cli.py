import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent / "cli"

js = (root / "script.js").read_text(encoding="utf-8")
stripped = re.sub(r"//[^\n]*", "", js)
stripped = re.sub(r"/\*.*?\*/", "", stripped, flags=re.S)
stripped = re.sub(r"`(?:[^`\\\\]|\\\\.)*`", '""', stripped, flags=re.S)
stripped = re.sub(r'"(?:[^"\\\\]|\\\\.)*"', '""', stripped)
stripped = re.sub(r"'(?:[^'\\\\]|\\\\.)*'", "''", stripped)
# strip regex literals: after ( , = : [ ! & | ? { ; or start-of-line
stripped = re.sub(r"(?<=[(,=:\[!&|?{;\n])\s*/(?:[^/\\\\\n\[]|\\\\.|\[(?:[^\]\\\\]|\\\\.)*\])+/[a-z]*", " null", stripped)
ok = True
for oc, cc in [("{", "}"), ("(", ")"), ("[", "]")]:
    o, c = stripped.count(oc), stripped.count(cc)
    status = "OK" if o == c else "MISMATCH"
    if o != c:
        ok = False
    print(f"JS {oc}{cc}: {o}/{c} {status}")

css = (root / "style.css").read_text(encoding="utf-8")
print("CSS {}:", css.count("{"), "/", css.count("}"),
      "OK" if css.count("{") == css.count("}") else "MISMATCH")

print("assets:",
      (root / "style.css").exists(),
      (root / "script.js").exists(),
      (root.parent / "img/seedcode.ico").exists())
print("RESULT:", "PASS" if ok else "FAIL")
