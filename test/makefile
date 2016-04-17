
OPTIONS = -pdf -outdir='.'

PYTHON = python3
ifeq ($(OS),Windows_NT)
	PYTHON = py -3
endif


all: *.pdf

%.pdf: .tmp/%.tex
	latexmk $(OPTIONS) $<

.tmp/%.tex: %.tex *.m
	mkdir -p .tmp/
	$(PYTHON) ../mlatex.py $<

clean:
	rm *.aux *.dvi *.pdf *.fls *.fdb_latexmk *.log
	rm -rf .tmp/
