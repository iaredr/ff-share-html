import glob, os, re, sys
d = os.path.dirname(os.path.abspath(__file__))
t = open(f"{d}/template.html", encoding="utf-8").read()
css = "".join(open(f, encoding="utf-8").read() + "\n" for f in sorted(glob.glob(f"{d}/parts/*.css")))
html = "".join(open(f, encoding="utf-8").read() + "\n" for f in sorted(glob.glob(f"{d}/parts/s*.html")))
out = t.replace("/*PARTS-CSS*/", css).replace("<!--SLIDES-->", html)
open(sys.argv[1] if len(sys.argv) > 1 else f"{d}/../index.html", "w", encoding="utf-8").write(out)
print("slides:", html.count('<section class="slide'))
