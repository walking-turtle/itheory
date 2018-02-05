.PHONY: all clean purge

TEX:=$(wildcard *.tex)
PDF:=${TEX:%.tex=%.pdf}
TEXMK:=lualatex --shell-escape >/dev/null
BIBTEX:=bibtex >/dev/null
PYTHON:=python3
TEXGEN:=$(wildcard code/*.tex.py)

all: ${PDF}

predictor_report.pdf: predictor_report.tex
	${TEXMK} ${@F:%.pdf=%.tex}
	${BIBTEX} ${@F:%.pdf=%}
	${TEXMK} ${@F:%.pdf=%.tex}
	${TEXMK} ${@F:%.pdf=%.tex}

code/%.tex: code/%.tex.py
	${PYTHON} $< > $@

predictor_slides.pdf: predictor_slides.tex ${TEXGEN:%.py=%}
	${TEXMK} ${@F:%.pdf=%.tex}
	${TEXMK} ${@F:%.pdf=%.tex}

%.pdf: %.tex
	${TEXMK} $<
	${TEXMK} $<

clean:
	${TEXMK} -c

purge:
	git clean -idx
