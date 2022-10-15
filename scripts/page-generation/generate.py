import os
import fileinput

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCRIPT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))

template = fileinput.input(SCRIPT_DIR + "\\template.html")
nav = fileinput.input(SCRIPT_DIR + "\\nav.html")
footer = fileinput.input(SCRIPT_DIR + "\\footer.html")

with open(ROOT_DIR + '\\index.html', 'w') as fout:
    content = fileinput.input(SCRIPT_DIR + "\\about.html")
    for line in template:
        fout.write(line)
    for line in nav:
        fout.write(line) 
    for line in content:
        fout.write(line)
    for line in footer:
        fout.write(line)
    content.close()
    
template = fileinput.input(SCRIPT_DIR + "\\template.html")
nav = fileinput.input(SCRIPT_DIR + "\\nav.html")
footer = fileinput.input(SCRIPT_DIR + "\\footer.html")

with open(ROOT_DIR + '\\projects\\index.html', 'w') as fout:
    content = fileinput.input(SCRIPT_DIR + "\\projects.html")
    for line in template:
        fout.write(line)
    for line in nav:
        fout.write(line) 
    for line in content:
        fout.write(line)
    for line in footer:
        fout.write(line)
    content.close()

template = fileinput.input(SCRIPT_DIR + "\\template.html")
nav = fileinput.input(SCRIPT_DIR + "\\nav.html")
footer = fileinput.input(SCRIPT_DIR + "\\footer.html")

with open(ROOT_DIR + '\\articles\\index.html', 'w') as fout:
    content = fileinput.input(SCRIPT_DIR + "\\articles.html")
    for line in template:
        fout.write(line)
    for line in nav:
        fout.write(line) 
    for line in content:
        fout.write(line)
    for line in footer:
        fout.write(line)
    content.close()
