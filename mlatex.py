import sys
import re
import hashlib
import os


def plot_generator(h, c):
    c = "clear all;\nclose all;\n" + c
    c += "\nexport_fig '.tmp/" + h + ".pdf' -transparent"
    return c


def gen_matlab(tex):
    matlab = ""
    m = re.search('\\\\matlabplot\{(.+?)\}\[(.+?)\]',tex, re.DOTALL)
    while m:
        filename = m.group(1)
        with open(filename, 'r') as matlab_file:
            matlab_code = matlab_file.read()
        matlab_hash = hashlib.md5(bytes(matlab_code,'utf-8')).hexdigest()
        if not (matlab_hash + '.pdf' in os.listdir('.tmp/')):
            matlab += plot_generator(matlab_hash, matlab_code)
        c = tex[:m.start()]
        c += "\n\\graphicspath{{.tmp/}}\n"
        c += "\\includegraphics[" + m.group(2) + "]{" + matlab_hash + ".pdf}"
        c += content[m.end():]
        tex = c
        m = re.search('\\\\matlabplot\{(.+?)\}\[(.+?)\]',tex, re.DOTALL)
    return (tex, matlab)


def run_matlab(c):
    filename = 'tmp_' + hashlib.md5(bytes(c,'utf-8')).hexdigest()
    with open(".tmp/" + filename + '.m', "w") as matlab_file:
        c = "addpath '../lib/export_fig/';\n" + c
        c += "\nexit;"
        matlab_file.write(c)
    cmd = 'matlab -wait -nospash -nodesktop -minimize -r "addpath .tmp;' + filename + '"'
    print(cmd)
    os.system(cmd)
    os.remove('.tmp/' + filename + '.m')



filename = os.path.basename(sys.argv[1])
with open(sys.argv[1]) as f:
    content = f.read()
(content, matlab_code) = gen_matlab(content)
with open('.tmp/' + filename, 'w') as f:
    f.write(content)
if matlab_code != "":
    run_matlab(matlab_code)
