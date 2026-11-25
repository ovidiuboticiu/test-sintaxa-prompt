#!/bin/sh
set -e
pandoc ../raport_test_sintaxa_prompt.md -f markdown+autolink_bare_uris+raw_tex --shift-heading-level-by=-1 --template=template.tex -o report.tex
xelatex -interaction=nonstopmode report.tex >/dev/null 2>&1 || true
xelatex -interaction=nonstopmode report.tex > build.log 2>&1 || true
grep -E "Overfull|Error|Missing character|Undefined" report.log | head -20
pdfinfo report.pdf | grep -E "Pages|Page size"
