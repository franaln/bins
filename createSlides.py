#! /usr/bin/env python2.7

import sys, os

usage = """Usage: createlides.py <project-name>
Esto crea una carpeta con ese nombre con <project-name>.tex, style.tex, physics.tex y el makefile."""

def makefile(projectName):
   content = """# Makefile created with createSlides

MAIN = %s

OBJS = $(MAIN).toc $(MAIN).aux $(MAIN).out $(MAIN).toc $(MAIN).log $(MAIN).snm $(MAIN).vrb $(MAIN).nav 


all: pdf
	rm -f $(OBJS)
	@echo "$@ done"


pdf: $(MAIN).tex
	@echo "Latexeando $(MAIN).tex"
	latex $(MAIN).tex
	latex $(MAIN).tex
	@dvips $(MAIN).dvi
	@ps2pdf $(MAIN).ps	


clean:
	@rm -rf $(MAIN).dvi
	@rm -rf $(MAIN).ps
	@rm -rf $(MAIN).pdf
""" % (projectName)

   return content


style = r"""% Beamer style

\usetheme{Boadilla}

% Packages                                                                                                                       
\usepackage[latin1]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{fancyhdr}
\usepackage{float}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{multirow}
\usepackage{verbatim}
\usepackage{colortbl}
\usepackage{fouriernc}
\usepackage{pstricks,pst-grad}
\usepackage{hyperref}
\usetikzlibrary{arrows,shapes,shadows}
\usetikzlibrary{fit}
\usetikzlibrary{backgrounds}

\renewcommand{\arraystretch}{1.5}

% Images folder
\graphicspath{{./images/}}

% Colors definition
\definecolor{mcolor}{HTML}{6666FF} % azulado
\definecolor{scolor}{HTML}{5ace60} % green 
\definecolor{mgray}{rgb}{0.41,0.41,0.41} % gray for names in titlepage

% Colors
\setbeamercolor*{frametitle}{bg=mcolor,fg=white}
\setbeamercolor*{item}{fg=scolor}
\setbeamercolor*{title}{fg=mcolor}
\setbeamercolor*{author}{fg=mgray}
\setbeamercolor*{institute}{fg=mgray}
\setbeamercolor*{date}{fg=mgray}
\setbeamercolor*{structure}{fg=mcolor}
\setbeamercolor*{footline}{fg=white, bg=mgray}

% Fonts
\renewcommand\mathfamilydefault{\rmdefault}
\renewcommand\familydefault{\rmdefault}
\setbeamerfont{title}{family*={fouriernc}, size=\fontsize{36}{40}}
\setbeamerfont{author}{family*={fouriernc}, size=\large}
\setbeamerfont{frametitle}{family*={fouriernc}, size*={15}{15}}
\setbeamerfont{block body}{size*={8}{0}, family*={fouriernc}}
\setbeamerfont{block title}{size*={8}{0}, family*={fouriernc}}

% Title page
\defbeamertemplate*{title page}{customized}[1][]
{
  \vspace{0.5cm}
  \usebeamercolor[fg]{title}\usebeamerfont{title}\inserttitle\par
  \vspace{1.5cm}
  \usebeamercolor[fg]{author}\usebeamerfont{author}\insertauthor\par
  \medskip
  \usebeamercolor[fg]{institute}\usebeamerfont{institute}\insertinstitute\par
  \vspace{1.4cm}
  \usebeamercolor[fg]{date}\usebeamerfont{date}\insertdate\par
}

% Frame title
\defbeamertemplate*{frametitle}{customized}[1][]
{
  \vspace{-0.05cm}
  \begin{beamercolorbox}[sep=.5em,wd=\paperwidth]{frametitle}
   {\bf \insertframetitle\hfill\color{scolor}{\small\insertframesubtitle\hspace{.1cm}}}
   \vspace{-.15cm}
  \end{beamercolorbox}
}

% Margins
\setbeamersize{text margin left=.2cm}
\setbeamersize{text margin right=.2cm}

% Items
\setbeamertemplate{itemize item}{\small\raise.2ex\hbox{\donotcoloroutermaths$\bullet$}}
\setbeamertemplate{itemize subitem}{\small\raise.1ex\hbox{\donotcoloroutermaths$\circ$}}
\setbeamertemplate{itemize subsubitem}{\scriptsize\raise.1ex\hbox{\donotcoloroutermaths$\bullet$}}
\setbeamertemplate{enumerate items}[default]

%% Blocks
%\setbeamertemplate{blocks}
%\newenvironment<>{varblock}[2][\textwidth]{ \begin{center} \begin{minipage}{#1} \setlength{\textwidth}{#1} \begin{actionenv}#3 \def\insertblocktitle{#2} \par \usebeamertemplate{block begin}} {\par \usebeamertemplate{block end} \end{actionenv} \end{minipage} \end{center} }

% Footer
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{
  \vspace{0.1cm}
  \hfill{\color{mgray} \insertframenumber/\inserttotalframenumber} \hspace*{0.12cm}
  \vspace*{0.12cm}
} 

% Color shapes
\tikzstyle{greenellipse}=[ellipse, thick, fill=green!30, anchor=base]
\tikzstyle{redellipse}=[ellipse, thick, fill=red!30, anchor=base]
\tikzstyle{bluerectangle}=[rectangle, thick, fill=mcolor!30, anchor=base]
\tikzstyle{greenellipse}=[ellipse, thick, fill=green, anchor=base]
\tikzstyle{blueellipse}=[ellipse, thick, fill=blue, anchor=base]
\tikzstyle{mellipse}=[ellipse, thick, fill=mcolor, anchor=base]
\tikzstyle{sellipse}=[ellipse, thick, fill=scolor, anchor=base]

%% Boxes
\newcommand{\boxSimple}[3]{\begin{center}\psframebox[#2]{\begin{minipage}[t][]{#1}#3\end{minipage}} \end{center}}
\newcommand{\boxDouble}[3]{\begin{center}\psdblframebox[#2]{\begin{minipage}[t][][t]{#1} #3 \end{minipage}}\end{center}}
\newcommand{\boxShadow}[3]{\begin{center}\psshadowbox[#2]{\begin{minipage}[t][][t]{#1} #3 \end{minipage}}\end{center}}

%% Different frames
\newenvironment{frame2columns}[3]{
  \begin{frame}
    \frametitle{#1}
    \begin{columns}[T]
      \column{0.5\textwidth} 
      #2 
      \column{0.5\textwidth}  
      #3
    \end{columns}
} {\end{frame}}
"""

physics = r"""%
% Physics (from atlasphysics)
%

\let\sst=\scriptscriptstyle
\chardef\letterchar=11
\chardef\otherchar=12
\chardef\eolinechar=5
%
%   Useful symbols for use in or out of math mode
%
\def\ra{\ensuremath{\rightarrow}}%  "GOES TO" arrow.
\def\la{\ensuremath{\leftarrow}}%   "GETS" arrow.
\let\rarrow=\ra
\let\larrow=\la
\def\lapprox{\ensuremath{\sim\kern-1em\raise 0.65ex\hbox{$<$}}}%  Or use \lsim
\def\rapprox{\ensuremath{\sim\kern-1em\raise 0.65ex\hbox{$>$}}}%  and \rsim.
\def\gam{\ensuremath{\gamma}}
\def\rts {\ensuremath{\sqrt{s}}}
\def\stat{\mbox{$\;$(stat.)}}
\def\syst{\mbox{$\;$(syst.)}}
%
%   Particle-antiparticle pair notations
%
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
%
%   e+e-, etc.
%
\def\ee{\ensuremath{e^+ e^-}}%
\def\epm{\ensuremath{e^{\pm}}}%
\def\epem{\ensuremath{e^+ e^-}}%
\def\mumu{\ensuremath{\mathrm{\mu^+ \mu^-}}}%
\def\tautau{\ensuremath{\mathrm{\tau^+ \tau^-}}}%
\let\muchless=\ll
\def\ll{\ensuremath{\ell^+ \ell^-}}%
\def\lnu{\ensuremath{\ell \nu}}%
%
%   New particle stuff
%
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
%
%   pi, pi0, pi+, pi-, pi+-, eta, eta1, etc.
%
\let\pii=\pi
\def\pi{\ensuremath{\pii}}%
\def\pizero{\ensuremath{\pii^0}}%
\def\piplus{\ensuremath{\pii^+}}%
\def\piminus{\ensuremath{\pii^-}}%
\def\pipm{\ensuremath{\pii^{\pm}}}%
\def\pimp{\ensuremath{\pii^{\mp}}}%
\let\etaa=\eta
\def\eta{\ensuremath{\etaa}}%
\def\etaprime{\ensuremath{\eta^{\sst\prime}}}%
%
%   Useful things for proton-proton physics
% 
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
\def\tjjb{\ensuremath{t \rightarrow jjb}}
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
\def\Amm{\ensuremath{A \rightarrow \mu\mu}}
\def\Ztau{\ensuremath{Z \rightarrow \tau\tau}}
\def\Wtau{\ensuremath{W \rightarrow \tau\nu}}
\def\Atau{\ensuremath{A \rightarrow \tau\tau}}
\def\Htau{\ensuremath{H \rightarrow \tau\tau}}
\def\begL{10$^{31}$~cm$^{-2}$~s$^{-1}$}
\def\lowL{10$^{33}$~cm$^{-2}$~s$^{-1}$}
\def\highL{10$^{34}$~cm$^{-2}$~s$^{-1}$}
\newcommand{\Rcone}{\ensuremath{R_{\mathrm{cone}}}} % Subscript roman not italic (EE)
%
%   Some useful units
%
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
 
"""


template = r"""\documentclass[center,10pt,cm]{beamer}

% Style and Atlas symbols
\input{style.tex}
\input{physics.tex}


% Title page
\title{ {\bf Title } }
\author{ Francisco Alonso }
\institute{\small UNLP - IFLP (CONICET)}
\date{ meeting  : :   \today }


\begin{document}
\centering

% Title
\begin{frame}[plain]
  \titlepage
\end{frame}

% Introduction
\begin{frame}{Overview}
  \begin{itemize}\itemsep.5cm\parsep.5cm
  \item Item
  \end{itemize}
\end{frame}

\begin{frame}{Title}{Subtitle}
\end{frame}

\begin{frame}{Title}{Subtitle}
\end{frame}

\begin{frame}{Conclusions}
\end{frame}

\end{document}

% itemize
% \begin{itemize}\itemsep0.5cm\topsep0.5cm
%   \item
% \end{itemize}

% figure
% \begin{figure}[H]
%   \centering
%   \includegraphics[width=\textwidth]{}
% \end{figure}

% table
% \begin{table}[htbp]
%   \footnotesize
%   \begin{tabular}{|c|c|}
%   \end{tabular}
% \end{table}

% color shapes
% \tikz[baseline] \node[\greenellipse] {texto};

% flechitas
% \tikzstyle{line} = [-latex',color=maincolor]
% \begin{figure}[h!]
%\begin{tikzpicture}[node distance = 2cm, auto]
%% Place nodes
%\node (sub) at  (2,1)    {{\color{green} Additional $0.3\%X_0$ after P2}};
%\node (sub2) at (2,0)    {{\color{complementary}      Remove $0.4\%X_0$ in P1}};
%\node (sub3) at (2,-1)   {{\color{blue} Additional $0.4\%X_0$ in P1}};
%\node (muo) at (-1,0) {3 samples};
%
%% Draw edges
%\path [line] (muo.east) edge [out=0, in=180] (sub.west);
%\path [line] (muo.east) edge [out=0, in=180] (sub2.west);
%\path [line] (muo.east) edge [out=0, in=180] (sub3.west);
%\end{tikzpicture}
%\end{figure}

% boxes
% \boxSimple{0.8\textwidth}{linewidth=.3mm,linecolor=bluemod,framesep=1em}{Text}

"""

def main():

   if len(sys.argv) < 2:
      print(usage)
      return 1

   projectName = sys.argv[1]

   # Create slides folder and the images folder inside
   try:
      os.makedirs(projectName + '/images' ) 
   except OSError as exception:
      print('Error. Directory exists?')
      return 1

   # Copy all the necessary files inside
   os.chdir(projectName)

   fo = open('makefile', 'wb')
   fo.write(makefile(projectName))
   fo.close()
   
   fo = open('physics.tex', 'wb')
   fo.write(physics)
   fo.close()
   
   fo = open('style.tex', 'wb')
   fo.write(style)
   fo.close()
   
   fo = open(projectName + '.tex', 'wb')
   fo.write(template)
   fo.close()

   return

if __name__ == '__main__':
   main()
