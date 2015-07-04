#! /usr/bin/env python3

import sys, os

usage = """Usage: slides.py name
creates directory \"name\" in the current directory with the following files: slides.tex, style.tex, physics.tex."""

style = r"""
% ----------
%  Packages
% ----------
\usepackage[latin1]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{fancyhdr}
\usepackage{float}
\usepackage{graphicx}

% -------------------------------
%  Optional packages (uncomment)
% -------------------------------
%\usepackage{multirow}
%\usepackage{verbatim}
%\usepackage{pstricks,pst-grad}
%\usepackage[percent]{overpic}
%\usepackage{hyperref} % links
%\usepackage{tikz}
%\usetikzlibrary{arrows,shapes,shadows,positioning}

\graphicspath{{./images/}}

% --------------
%  Style config
% --------------
\usetheme{Boadilla}
\renewcommand{\arraystretch}{1.5}

\setbeamersize{text margin left=.2cm}
\setbeamersize{text margin right=.2cm}

\definecolor{mcolor}{HTML}{37437F} % azulado
\definecolor{mgray}{HTML}{4D4D4D}  % gray
\definecolor{sgray}{HTML}{9E9E9E}
\definecolor{agray}{HTML}{1C1C1C}
\definecolor{mred}{HTML}{E63753}

\setbeamercolor*{frametitle}{bg=mcolor,fg=white}
\setbeamercolor*{item}{fg=agray}
\setbeamercolor*{title}{fg=mcolor}
\setbeamercolor*{author}{fg=mgray}
\setbeamercolor*{institute}{fg=mgray}
\setbeamercolor*{date}{fg=mgray}
\setbeamercolor*{structure}{fg=mcolor}
\setbeamercolor*{footline}{fg=white, bg=mgray}

\renewcommand\mathfamilydefault{\rmdefault}
\renewcommand\familydefault{\rmdefault}
\setbeamerfont{title}{family*={fouriernc}, size=\fontsize{30}{32}}
\setbeamerfont{author}{family*={fouriernc}, size=\large}
\setbeamerfont{block body}{size*={8}{0}, family*={fouriernc}}
\setbeamerfont{block title}{size*={8}{0}, family*={fouriernc}}

\setbeamertemplate{itemize item}{\tiny\raise.2ex\hbox{\donotcoloroutermaths$\bullet$}}
\setbeamertemplate{itemize subitem}{\tiny\raise.1ex\hbox{\donotcoloroutermaths$\circ$}}
\setbeamertemplate{itemize subsubitem}{\tiny\raise.1ex\hbox{\donotcoloroutermaths$\bullet$}}
\setbeamertemplate{enumerate items}[default]

% ------------
%  Title page
% ------------
\defbeamertemplate*{title page}{customized}[1][]
{
  \centering
  \begin{minipage}[t][5cm][c]{\textwidth}
  \centering
  \usebeamercolor[fg]{title}\usebeamerfont{title}\inserttitle\par
  \end{minipage}
  \begin{minipage}[t][3.6cm][c]{\textwidth}
  \centering
  \usebeamercolor[fg]{author}\usebeamerfont{author}\insertauthor\par
  \medskip
  \usebeamercolor[fg]{institute}\usebeamerfont{institute}\insertinstitute\par
  \end{minipage}
  \begin{minipage}[t][1cm][c]{\textwidth}
  \centering
  \usebeamercolor[fg]{date}\usebeamerfont{date}\insertdate\par
  \end{minipage}
}

% -------------
%  Frame title
% -------------
\defbeamertemplate*{frametitle}{customized}[1][]
{
  \vspace{-0.05cm}
  \begin{beamercolorbox}[sep=.5em,wd=\paperwidth]{frametitle}
   {\bf \Large \insertframetitle\hfill{\small\insertframesubtitle\hspace{.1cm}}}
  \vspace{-.10cm}
  \end{beamercolorbox}
}

% --------
%  Footer
% --------
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{
  \vspace{0.1cm}
  \hfill{\color{mgray} \insertframenumber/\inserttotalframenumber} \hspace*{0.12cm}
  \vspace*{0.12cm}
}

% -------------
%  Tikz shapes
% -------------
\newcommand{\redrectangle}[1]{\tikz[baseline] \node[rectangle,thick,fill=red!30,anchor=base]{#1};}
\newcommand{\bluerectangle}[1]{\tikz[baseline] \node[rectangle,thick,fill=mcolor!30,anchor=base]{#1};}
\newcommand{\greenrectangle}[1]{\tikz[baseline] \node[rectangle,thick,fill=green!30,anchor=base]{#1};}
\newcommand{\grayrectangle}[1]{\tikz[baseline] \node[rectangle,thick,fill=black!30,anchor=base]{#1};}
\newcommand{\tikztag}[1]{\tikz[baseline] \node (#1) {};}

% -----------------
%  Custom commands
% -----------------
\newcommand{\boxd}[2]{\begin{center}\psframebox[linewidth=.1mm,linecolor=mcolor,framesep=0.5em]{\begin{minipage}[t][]{#1\textwidth}#2\end{minipage}} \end{center}}
\newcommand{\centered}[1]{\begin{center} #1 \end{center}}
\newcommand{\cheader}[1]{\begin{center} \large \bf \color{sgray} #1 \end{center}}
\newcommand{\ptitle}[1]{\begin{flushleft}{\large \bf #1}\end{flushleft}}
\newcommand{\onlytitle}[1]{\begin{center} \fontsize{5cm}{1em}\selectfont \bf \color{sgray} #1 \end{center}}
\newcommand{\oneitem}[1]{\begin{itemize} \item #1 \end{itemize}}
\newcommand{\colorarrow}{{\color{mcolor}\ensuremath{\to}}}
\newcommand{\colorify}[1]{{\color{mcolor} #1}}
\newcommand{\beginbackup}{\begin{frame}\onlytitle{Backup}\end{frame}}
\newcommand{\fix}[1]{{\color{mred} #1}}
\newcommand{\focus}[1]{{\color{mred} #1}}
\newcommand{\hr}{\begin{center} \line(1,0){350} \end{center}}
\newcommand{\img}[2]{\includegraphics[width=#1\textwidth]{#2}}
\newcommand{\overimg}[4]{\begin{overpic}[width=#1\textwidth]{#2} \put(#3){\tiny #4} \end{overpic}}
\newcommand{\vsp}{\vspace{0.5cm}}

"""

physics = r"""%
% Physics symbols (from atlasphysics)
%
\let\sst=\scriptscriptstyle
\chardef\letterchar=11
\chardef\otherchar=12
\chardef\eolinechar=5

\def\ra{\ensuremath{\rightarrow}}%  "GOES TO" arrow.
\def\la{\ensuremath{\leftarrow}}%   "GETS" arrow.
\def\gam{\ensuremath{\gamma}}
\def\rts {\ensuremath{\sqrt{s}}}
\def\stat{\mbox{$\;$(stat.)}}
\def\syst{\mbox{$\;$(syst.)}}

\def\antibar#1{\ensuremath{#1\bar{#1}}}
\def\tbar{\ensuremath{\bar{t}}}
\def\ttbar{\antibar{t}}
\def\bbar{\ensuremath{\bar{b}}}
\def\bbbar{\antibar{b}}
\def\cbar{\ensuremath{\bar{c}}}
\def\ccbar{\antibar{c}}
\def\sbar{\ensuremath{\bar{s}}}
\def\ssbar{\antibar{s}}
\def\ubar{\ensuremath{\bar{u}}}
\def\uubar{\antibar{u}}
\def\dbar{\ensuremath{\bar{d}}}
\def\ddbar{\antibar{d}}
\def\fbar{\ensuremath{\bar{f}}}
\def\ffbar{\antibar{f}}
\def\qbar{\ensuremath{\bar{q}}}
\def\qqbar{\antibar{q}}
\def\nbar{\ensuremath{\bar{\nu}}}
\def\nnbar{\antibar{\nu}}
\def\ee{\ensuremath{e^+ e^-}}%
\def\epm{\ensuremath{e^{\pm}}}%
\def\epem{\ensuremath{e^+ e^-}}%
\def\mumu{\ensuremath{\mathrm{\mu^+ \mu^-}}}%
\def\tautau{\ensuremath{\mathrm{\tau^+ \tau^-}}}%
\let\muchless=\ll
\def\ll{\ensuremath{\ell^+ \ell^-}}%
\def\lnu{\ensuremath{\ell \nu}}%

\def\Azero{\ensuremath{A^0}}%
\def\hzero{\ensuremath{h^0}}%
\def\Hzero{\ensuremath{H^0}}%
\def\Hboson{\ensuremath{H}}%
\def\Hplus{\ensuremath{H^+}}%
\def\Hminus{\ensuremath{H^-}}%
\def\Hpm{\ensuremath{H^{\pm}}}%
\def\Hmp{\ensuremath{H^{\mp}}}%
\def\susy#1{\ensuremath{\tilde{#1}}}%
\def\ellell{\ensuremath{\mathrm{\ell^+ \ell^-}}}%
\def\ggino{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi$}}}}
\def\chinop{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^+$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^+$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^+$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^+$}}}}
\def\chinom{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^-$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^-$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^-$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^-$}}}}
\def\chinopm{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^\pm$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^\pm$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^\pm$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^\pm$}}}}
\def\chinomp{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^\mp$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^\mp$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^\mp$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^\mp$}}}}
\def\chinoonep{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^+_1$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^+_1$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^+_1$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^+_1$}}}}
\def\chinoonem{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^-_1$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^-_1$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^-_1$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^-_1$}}}}
\def\chinoonepm{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^\pm_1$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^\pm_1$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^\pm_1$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^\pm_1$}}}}
\def\chinotwop{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^+_2$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^+_2$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^+_2$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^+_2$}}}}
\def\chinotwom{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^-_2$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^-_2$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^-_2$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^-_2$}}}}
\def\chinotwopm{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^\pm_2$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^\pm_2$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^\pm_2$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^\pm_2$}}}}
\def\nino{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^0$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^0$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^0$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^0$}}}}
\def\ninoone{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^0_1$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^0_1$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^0_1$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^0_1$}}}}
\def\ninotwo{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^0_2$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^0_2$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^0_2$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^0_2$}}}}
\def\ninothree{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^0_3$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^0_3$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^0_3$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^0_3$}}}}
\def\ninofour{\ensuremath{\mathchoice%
      {\displaystyle\raise.4ex\hbox{$\displaystyle\tilde\chi^0_4$}}%
         {\textstyle\raise.4ex\hbox{$\textstyle\tilde\chi^0_4$}}%
       {\scriptstyle\raise.3ex\hbox{$\scriptstyle\tilde\chi^0_4$}}%
 {\scriptscriptstyle\raise.3ex\hbox{$\scriptscriptstyle\tilde\chi^0_4$}}}}
\def\gravino{\ensuremath{\tilde{G}}}%
\def\Zprime{\ensuremath{Z^\prime}}
\def\Zstar{\ensuremath{Z^{*}}}
\def\squark{\ensuremath{\tilde{q}}}
\def\squarkL{\ensuremath{\tilde{q}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\squarkR{\ensuremath{\tilde{q}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\gluino{\ensuremath{\tilde{g}}}
\def\stop{\ensuremath{\tilde{t}}}
\def\stopone{\ensuremath{\tilde{t}_1}}
\def\stoptwo{\ensuremath{\tilde{t}_2}}
\def\stopL{\ensuremath{\tilde{t}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\stopR{\ensuremath{\tilde{t}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\sbottom{\ensuremath{\tilde{b}}}
\def\sbottomone{\ensuremath{\tilde{b}_1}}
\def\sbottomtwo{\ensuremath{\tilde{b}_2}}
\def\sbottomL{\ensuremath{\tilde{b}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\sbottomR{\ensuremath{\tilde{b}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\slepton{\ensuremath{\tilde{\ell}}}
\def\sleptonL{\ensuremath{\tilde{\ell}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\sleptonR{\ensuremath{\tilde{\ell}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\sel{\ensuremath{\tilde{e}}}
\def\selL{\ensuremath{\tilde{e}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\selR{\ensuremath{\tilde{e}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\smu{\ensuremath{\tilde{\mu}}}
\def\smuL{\ensuremath{\tilde{\mu}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\smuR{\ensuremath{\tilde{\mu}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\stau{\ensuremath{\tilde{\tau}}}
\def\stauL{\ensuremath{\tilde{\tau}_{\mathrm{L}}}} % Subscript roman not italic (EE)
\def\stauR{\ensuremath{\tilde{\tau}_{\mathrm{R}}}} % Subscript roman not italic (EE)
\def\stauone{\ensuremath{\tilde{\tau}_1}}
\def\stautwo{\ensuremath{\tilde{\tau}_2}}
\def\snu{\ensuremath{\tilde{\nu}}}

\def\pt{\ensuremath{p_{\mathrm{T}}}} % Subscript roman not italic (EE)
\def\pT{\ensuremath{p_{\mathrm{T}}}} % Subscript roman not italic (EE)
\def\et{\ensuremath{E_{\mathrm{T}}}} % Subscript roman not italic (EE)
\def\eT{\ensuremath{E_{\mathrm{T}}}} % Subscript roman not italic (EE)
\def\ET{\ensuremath{E_{\mathrm{T}}}} % Subscript roman not italic (EE)
\def\HT{\ensuremath{H_{\mathrm{T}}}} % Subscript roman not italic (EE)
\def\ptsq{\ensuremath{p^2_{\mathrm{T}}}} % Fixed so it works correctly (EE)

\def\degr{\ensuremath{^\circ}} % Removed mbox - caused problems and not needed (EE)
\def\abseta{\ensuremath{|\eta|}}
\def\Hgg{\ensuremath{H\to\gamma\gamma}}
\def\mh{\ensuremath{m_h}}
\def\mW{\ensuremath{m_W}}
\def\mZ{\ensuremath{m_Z}}
\def\mH{\ensuremath{m_H}}
\def\mA{\ensuremath{m_A}}
\def\MET{\ensuremath{E_{\mathrm{T}}^{\mathrm{miss}}}} % Sub/superscript roman not italic (EE)
\def\met{\ensuremath{E_{\mathrm{T}}^{\mathrm{miss}}}} % Sub/superscript roman not italic (EE)
\def\Wjj{\ensuremath{W \rightarrow jj}}
\def\Hbb{\ensuremath{H \rightarrow b\bar b}}
\def\Zmm{\ensuremath{Z \rightarrow \mu\mu}}
\def\Zee{\ensuremath{Z \rightarrow ee}}
\def\Zll{\ensuremath{Z \rightarrow \ell\ell}}
\def\Wln{\ensuremath{W \rightarrow \ell\nu}}
\def\Wen{\ensuremath{W \rightarrow e\nu}}
\def\Wmn{\ensuremath{W \rightarrow \mu\nu}}
\def\Hllll{\ensuremath{H \rightarrow ZZ^{(*)} \rightarrow \mu\mu\mu\mu}}
\def\Hmmmm{\ensuremath{H \rightarrow \mu\mu\mu\mu}}
\def\Heeee{\ensuremath{H \rightarrow eeee}}
\def\Ztau{\ensuremath{Z \rightarrow \tau\tau}}
\def\Wtau{\ensuremath{W \rightarrow \tau\nu}}
\def\Atau{\ensuremath{A \rightarrow \tau\tau}}
\newcommand{\Rcone}{\ensuremath{R_{\mathrm{cone}}}} % Subscript roman not italic (EE)

\def\TeV{\ifmmode {\mathrm{\ Te\kern -0.1em V}}\else
                   \textrm{Te\kern -0.1em V}\fi}%
\def\GeV{\ifmmode {\mathrm{\ Ge\kern -0.1em V}}\else
                   \textrm{Ge\kern -0.1em V}\fi}%
\def\MeV{\ifmmode {\mathrm{\ Me\kern -0.1em V}}\else
                   \textrm{Me\kern -0.1em V}\fi}%
\def\keV{\ifmmode {\mathrm{\ ke\kern -0.1em V}}\else
                   \textrm{ke\kern -0.1em V}\fi}%
\def\eV{\ifmmode  {\mathrm{\ e\kern -0.1em V}}\else
                   \textrm{e\kern -0.1em V}\fi}%
\let\tev=\TeV
\let\gev=\GeV
\let\mev=\MeV
\let\kev=\keV
\let\ev=\eV

\def\tagprobe{tag \& probe}
\def\RT{\ensuremath{R_T^2}}
\def\dphijetmet{\ensuremath{\Delta\phi(\text{jet},\amet)}}
\def\dphigamjet{\ensuremath{\Delta\phi(\gam, \text{jet})}}
"""

template = r"""
\documentclass[center,10pt,cm]{beamer}
\usepackage{etex}

\input{style.tex}
\input{physics.tex}

\title{\bf Title}
\author{Francisco Alonso}
\institute{\small UNLP}
\date{meeting - \today}

\begin{document}
\centering

\begin{frame}[plain]
  \titlepage
\end{frame}

\begin{frame}{Title}
\end{frame}

\end{document}
"""


def main():

   if len(sys.argv) < 2:
      print(usage)
      return 1

   project_name = sys.argv[1]

   # create slides dir and images dir inside
   try:
      os.makedirs(project_name + '/images' )
   except OSError as exception:
      print('\022[31mError. Directory exists?\033[0m')
      return 1

   # create all the necessary files inside
   os.chdir(project_name)

   with open('physics.tex', 'wb') as fo:
      fo.write(bytes(physics, 'utf-8'))

   with open('style.tex', 'wb') as fo:
      fo.write(bytes(style, 'utf-8'))

   with open('slides.tex', 'wb') as fo:
      fo.write(bytes(template, 'utf-8'))

   print('\033[92m# Slides created in {0}\033[0m'.format(project_name))

   return

if __name__ == '__main__':
   main()