default: workout.pdf

%.pdf: %.tex
	pdflatex $<
	rm $< $*.aux $*.log

%.tex: strength.py
	python $< > $@

clean:
	-rm *.aux *.log *.pdf

.PHONY: default clean
