.PHONY: all clean purge

TEX:=$(wildcard *.tex)
PDF:=${TEX:%.tex=%.pdf}
TEXMK:=latexmk -lualatex

all: ${PDF}

%.pdf: %.tex
	${TEXMK} $<

clean:
	${TEXMK} -c

purge:
	git clean -idx
