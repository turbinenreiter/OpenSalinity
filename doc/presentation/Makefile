all:
	cp ~/Documents/Semesterarbeit/OpenSalinity/doc/presentation/biovt.beamer ~/.pandoc/templates/biovt.beamer
	pandoc -t beamer --template biovt -s -S presentation.md -o presentation.pdf

tex:
	cp ~/Documents/Semesterarbeit/OpenSalinity/doc/presentation/biovt.beamer ~/.pandoc/templates/biovt.beamer
	pandoc -t beamer --template biovt -s -S presentation.md -o presentation.tex
	xelatex presentation.tex
	rm *aux *log *out *toc *snm *nav

#pandoc -N --template=mytemplate.tex --variable mainfont="Palatino" --variable sansfont="Helvetica" --variable monofont="Menlo" --variable fontsize=12pt --variable version=1.17.2 outline.md --latex-engine=xelatex --toc -o outline.pdf

#--variable mainfont="Source Serif Pro" --variable sansfont="Source Sans Pro" --variable monofont="Source Code Pro"
