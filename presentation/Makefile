PDF=main.pdf

.PHONY: all clean

all:
	lualatex main.tex
	lualatex main.tex

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.nav *.snm *.vrb $(PDF)
