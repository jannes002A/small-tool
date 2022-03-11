#!/bin/python

from csv import reader
import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', default='', help='name of txt file')
parser.add_argument('-l', default = '', help='use produce tex')
args = parser.parse_args()

# open file in read mode
name = args.n
path = '..'


def get_list():
    with open(f'{path}/data/{name}.txt', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        output = ''
        for i,row in enumerate(csv_reader):
        # row variable is a list that represents a row in csv
            if row:
                output += ('{' + '"id":' + str(i+1) + ', "isDone": false, "title":"' + str(row[0]) +'"},')

        output = str('[') + output[:-1] +']'
        with open(f'{path}/res/{name}.txt','w') as file:
            file.write(output)


def get_latex():

    with open(f'{path}/data/{name}.txt', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        output = ''
        for row in csv_reader:
        # row variable is a list that represents a row in csv
            if row:
                output += '\item '+ str(row[0]) +"\n"
        output = output[:-2]

        begin_texfile=r"""
\documentclass[a4paper,british]{article}
\usepackage{babel}
\usepackage[utf8]{inputenc} 
\usepackage{enumitem,amssymb}
\newlist{todolist}{itemize}{2}
\setlist[todolist]{label=$\square$}
\usepackage{pifont}
\newcommand{\cmark}{\ding{51}}%
\newcommand{\xmark}{\ding{55}}%
\newcommand{\done}{\rlap{$\square$}{\raisebox{2pt}{\large\hspace{1pt}\cmark}}%
\hspace{-2.5pt}}
\newcommand{\wontfix}{\rlap{$\square$}{\large\hspace{1pt}\xmark}}
\begin{document}
\title{ToDo List}
\date{\today}
\author{List Maker}
\maketitle
\begin{itemize}
"""
        list_name = r"""\begin{todolist}
"""

        end_texfile=r"""
\end{todolist}
\end{itemize}
\end{document}"""

        texfile = begin_texfile +f"\item {name} \n" + list_name + output + end_texfile
        with open(f'{path}/res/{name}.tex','w') as file:
            file.write(texfile)

        bash_command = f'pdflatex ../res/{name}.tex'
        subprocess.run(bash_command.split())

if __name__ == '__main__':
    get_list()
    if args.l:
        get_latex()
