#!/usr/bin/env python3
"""Build the public CV PDF from the site's own data files.

Usage:  python3 scripts/build_cv.py
Reads:  _config.yml, _data/cv.yml, _data/publications.yml, _data/teaching.yml, _data/students.yml
Writes: cv_source/CV_Pallab_Ghosh.tex and assets/cv/CV_Pallab_Ghosh.pdf (needs pdflatex on PATH)

Policy (owner's decisions, September 2026): no mobile number; no journal names for
papers under review or in revision; author order as published; Pallab in bold.
"""
import datetime, os, re, shutil, subprocess, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

cfg = yaml.safe_load(open("_config.yml"))
cv = yaml.safe_load(open("_data/cv.yml"))
pubs = yaml.safe_load(open("_data/publications.yml"))
teaching = yaml.safe_load(open("_data/teaching.yml"))
students = yaml.safe_load(open("_data/students.yml"))
me = cfg["author"]["name"]


def tex(s):
    """Escape LaTeX special characters in plain text."""
    if s is None:
        return ""
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    return s


def authors_line(p):
    return ", ".join(r"\textbf{%s}" % tex(a) if a == me else tex(a) for a in p["authors"])


def coauthors(p):
    others = [a for a in p["authors"] if a != me]
    return (" with " + tex(", ".join(others))) if others else ""


def pub_item(p):
    venue = r"\emph{%s}" % tex(p["journal"])
    bits = [venue, tex(p.get("year"))]
    if p.get("volume"):
        v = tex(p["volume"]) + ("(%s)" % tex(p["issue"]) if p.get("issue") else "")
        bits.append(v)
    if p.get("pages"):
        bits.append(tex(p["pages"]).replace("-", "--"))
    title = tex(p["title"])
    sep = "" if title.endswith(("?", "!")) else "."
    line = r"\item %s. %s%s %s." % (authors_line(p), title, sep, ", ".join(b for b in bits if b))
    if p.get("doi"):
        line += r" \href{https://doi.org/%s}{doi:%s}" % (p["doi"], tex(p["doi"]))
    if p.get("note"):
        line += r" {\footnotesize %s}" % tex(p["note"])
    return line


published = [p for p in pubs if p["status"] in ("published", "forthcoming")]
commentary = [p for p in pubs if p["status"] == "commentary"]
by_area = {"labor": [], "econometrics": [], "health": []}
for p in published:  # file order: newest first within each area, same as the web page
    by_area[p["area"]].append(p)
area_names = {"labor": "Labor and development economics", "econometrics": "Econometrics", "health": "Health economics and policy"}

status_names = [("rr", "Revise and resubmit"), ("reject_resubmit", "Reject and resubmit"), ("under_review", "Under review"), ("working", "Working papers"), ("in_progress", "Work in progress")]

L = []
A = L.append
A(r"""\documentclass[10.5pt]{article}
\usepackage[margin=0.85in]{geometry}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage[hidelinks,pdfauthor={Pallab Ghosh},pdftitle={Curriculum Vitae, Pallab Ghosh}]{hyperref}
\definecolor{accent}{HTML}{7A1F1F}
\hypersetup{colorlinks=true,urlcolor=accent,linkcolor=accent}
\titleformat{\section}{\large\bfseries\color{accent}}{}{0pt}{}[\vspace{-0.4em}\rule{\textwidth}{0.4pt}]
\titlespacing*{\section}{0pt}{1.1em}{0.5em}
\titleformat{\subsection}{\normalsize\bfseries}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{0.7em}{0.25em}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.25em}
\setlist[enumerate]{leftmargin=2em,itemsep=2pt,topsep=2pt}
\setlist[itemize]{leftmargin=1.4em,itemsep=2pt,topsep=2pt}
\pagestyle{plain}
\newcommand{\cvrow}[2]{\noindent\begin{tabularx}{\textwidth}{@{}X r@{}} #1 & {\small\color{gray} #2} \end{tabularx}\par}
\begin{document}
""")
A(r"\begin{center}{\LARGE\bfseries %s}\\[0.35em]" % tex(me))
A(r"{\small %s\quad\textbar\quad %s}\\[0.15em]" % (tex(cfg["author"]["title"]), tex(cfg["author"]["role2"])))
A(r"{\small %s, %s}\\[0.15em]" % (tex(cfg["author"]["department"]), tex(cfg["author"]["university"])))
A(r"{\small %s, %s, %s}\\[0.15em]" % (tex(cfg["author"]["address_line1"]), tex(cfg["author"]["office"]), tex(cfg["author"]["address_line2"])))
A(r"{\small \href{mailto:%s}{%s}\quad\textbar\quad Office %s\quad\textbar\quad \href{%s}{%s}\quad\textbar\quad ORCID \href{https://orcid.org/%s}{%s}}" % (
    cfg["author"]["email"], tex(cfg["author"]["email"]), tex(cfg["author"]["phone"]), cfg["url"], tex(cfg["url"].replace("https://", "")), cfg["profiles"]["orcid"], tex(cfg["profiles"]["orcid"])))
A(r"\end{center}")

A(r"\section{Education}")
for e in cv["education"]:
    detail = (r"\\ {\small\itshape %s}" % tex(e["detail"])) if e.get("detail") else ""
    A(r"\cvrow{\textbf{%s}, %s%s}{%s}" % (tex(e["degree"]), tex(e["school"]), detail, tex(e["when"])))

A(r"\section{Employment}")
for e in cv["employment"]:
    A(r"\cvrow{\textbf{%s}\\ {\small %s}}{%s}" % (tex(e["title"]), tex(e["org"]), tex(e["when"])))

A(r"\section{Research interests}")
A("Econometrics, labor economics, health economics, and development economics.")

A(r"\section{Publications (%d)}" % (len(published) + len(commentary)))
A(r"{\small %d refereed articles and %d editor reviewed commentary. Author lists are given as published, in published order.}\par" % (len(published), len(commentary)))
counter = 0
for key in ("labor", "econometrics", "health"):
    A(r"\subsection{%s}" % area_names[key])
    A(r"\begin{enumerate}[start=%d]" % (counter + 1))
    for p in by_area[key]:
        A(pub_item(p)); counter += 1
    A(r"\end{enumerate}")
if commentary:
    A(r"\subsection{Commentary}")
    A(r"\begin{enumerate}[start=%d]" % (counter + 1))
    for p in commentary:
        A(pub_item(p)); counter += 1
    A(r"\end{enumerate}")

A(r"\section{Manuscripts under review, in revision, and in progress}")
for key, name in status_names:
    items = [p for p in pubs if p["status"] == key]
    if not items:
        continue
    A(r"\subsection{%s}" % name)
    A(r"\begin{enumerate}")
    for p in items:
        A(r"\item %s%s" % (tex(p["title"]), coauthors(p)))
    A(r"\end{enumerate}")

A(r"\section{Invited talks and conference presentations}")
A(r"\begin{itemize}")
for t in cv["talks"]:
    A(r"\item[\textbf{%s}] %s" % (tex(t["year"]), tex(t["venues"])))
A(r"\end{itemize}")

A(r"\section{Awards and honors}")
A(r"\begin{itemize}")
for a in cv["awards"]:
    A(r"\item[\textbf{%s}] %s" % (tex(a["year"]), tex(a["text"])))
A(r"\end{itemize}")

A(r"\section{Funding and leave}")
A(r"\begin{itemize}")
for f in cv["funding"]:
    A(r"\item %s" % tex(f["text"]))
A(r"\end{itemize}")

A(r"\section{Refereeing and professional service}")
A(tex(cv["refereeing"]["summary"]) + r"\par")
A(r"{\small " + "; ".join(r"\emph{%s}%s" % (tex(j["name"]), (" (%d)" % j["n"]) if j["n"] > 1 else "") for j in cv["refereeing"]["journals"]) + ".}")

A(r"\section{Departmental and university service}")
for s in cv["service"]:
    detail = (r"\\ {\small %s}" % tex(s["detail"])) if s.get("detail") else ""
    A(r"\cvrow{%s%s}{%s}" % (tex(s["text"]), detail, tex(s["when"])))

A(r"\section{Teaching}")
for group in teaching:
    A(r"\subsection{%s}" % tex(group["level"]))
    for c in group["courses"]:
        code = c["code"] if re.match(r"^[A-Z]{2,4} \d", str(c["code"])) else ""
        A(r"\cvrow{%s {\small\color{gray} %s}}{%s}" % (tex(c["title"]), tex(code), tex(c["when"])))
A(r"\subsection{Syracuse University}")
A(r"\cvrow{Labor Economics}{Summer 2012}")

A(r"\section{Doctoral students, chair or co-chair}")
for s in students["advisees"]:
    A(r"\cvrow{\textbf{%s}, %s (%s)\\ {\small %s}}{%s}" % (tex(s["name"]), tex(s["field"]), tex(s["role"]), tex(s["placement"]), tex(s["years"])))

A(r"\section{Doctoral dissertation committees (%d)}" % len(students["committees"]))
A(r"\begin{longtable}{@{}p{0.45\textwidth} p{0.33\textwidth} p{0.18\textwidth}@{}}")
for s in students["committees"]:
    A(r"%s & %s & %s \\" % (tex(s["name"]), tex(s["field"]), tex(s["year"])))
A(r"\end{longtable}")

A(r"\section{Undergraduate honors and master's research students}")
A(", ".join("%s (%s)" % (tex(s["name"]), tex(s["year"])) for s in students["honors"]) + r".\par")

A(r"\vspace{1em}{\small\color{gray} Last updated %s. The current version of this CV is at \href{%s/cv/}{%s/cv/}.}" % (datetime.date.today().strftime("%B %-d, %Y"), cfg["url"], tex(cfg["url"].replace("https://", ""))))
A(r"\end{document}")

os.makedirs("cv_source", exist_ok=True)
texpath = "cv_source/CV_Pallab_Ghosh.tex"
open(texpath, "w").write("\n".join(L))
print("wrote", texpath)

if shutil.which("pdflatex") is None:
    print("pdflatex not found; TeX written but PDF not built", file=sys.stderr)
    sys.exit(1)
for _ in range(2):
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory=cv_source", texpath], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], file=sys.stderr)
        sys.exit(1)
shutil.copy("cv_source/CV_Pallab_Ghosh.pdf", "assets/cv/CV_Pallab_Ghosh.pdf")
for ext in (".aux", ".log", ".out"):
    try:
        os.remove("cv_source/CV_Pallab_Ghosh" + ext)
    except FileNotFoundError:
        pass
print("built assets/cv/CV_Pallab_Ghosh.pdf")
