.PHONY: all clean purge

TEX:=$(wildcard *.tex)
PDF:=${TEX:%.tex=%.pdf}
TEXMK:=lualatex --shell-escape
BIBTEX:=bibtex
TEXGEN:=$(wildcard code/*.tex.py)

all: ${PDF}

predictor_report.pdf: predictor_report.tex
	${TEXMK} ${@F:%.pdf=%.tex}
	${BIBTEX} ${@F:%.pdf=%}
	${TEXMK} ${@F:%.pdf=%.tex}
	${TEXMK} ${@F:%.pdf=%.tex}

code/%.tex: code/%.tex.py
	python3 $< > $@

predictor_slides.pdf: predictor_slides.tex ${TEXGEN:%.py=%}
	${TEXMK} $<
	${TEXMK} $<

%.pdf: %.tex
	${TEXMK} $<
	${TEXMK} $<

clean:
	${TEXMK} -c

purge:
	git clean -idx
