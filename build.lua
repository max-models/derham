module = "derham"
sourcefiles = {"derham.sty", "derham.tex", "README.md", "CHANGELOG.md", "LICENSE", "examples/*.tex"}
installfiles = {"derham.sty"}
typesetfiles = {"derham.tex"}
typesetexe = "pdflatex"
checkengines = {"pdftex", "luatex", "xetex"}
checkruns = 1
testfiledir = "testfiles"
