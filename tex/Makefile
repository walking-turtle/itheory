.PHONY: all clean purge

TEX:=$(wildcard *.tex)
PDF:=${TEX:%.tex=%.pdf}
TEXMK:=lualatex --shell-escape

all: ${PDF}

%.pdf: %.tex
	${TEXMK} $<
	bibtex $*
	${TEXMK} $<
	${TEXMK} $<

clean:
	${TEXMK} -c

purge:
	git clean -idx
