TEX  = pdflatex
BIB  = bibtex
MAIN = main

.PHONY: all clean

all:
	$(TEX) $(MAIN)
	$(BIB) $(MAIN)
	$(TEX) $(MAIN)
	$(TEX) $(MAIN)
	cp $(MAIN).pdf ../docs/$(MAIN).pdf

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).bbl $(MAIN).blg \
	      $(MAIN).out $(MAIN).pdf $(MAIN).toc $(MAIN).lof \
	      $(MAIN).lot $(MAIN).nav $(MAIN).snm $(MAIN).synctex.gz
