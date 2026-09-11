\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tudelft-report}[2026/06/01 v2.0 TU Delft report class]

\DeclareKeys[tudelft-report] {
  fourier.if         = @fourier,
  print.if           = @print,
}

% all other options are passed on to scrbook
\DeclareUnknownKeyHandler[tudelft-report]
  {\PassOptionsToClass{\CurrentOption}{scrbook}}

\ProcessKeyOptions[tudelft-report]

\LoadClass[
  10pt,
  headsepline=true,
]{scrbook}

\if@print
  \NewDocumentCommand{\IfPrintTF}{m m}{#1}
\else
  \NewDocumentCommand{\IfPrintTF}{m m}{#2}
\fi

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{ifluatex}

\RequirePackage{scrlayer-scrpage}
\RequirePackage[flushmargin,hang]{footmisc}
\RequirePackage{geometry}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{xcolor}

\RequirePackage{tudelft-color}
\RequirePackage{tudelft-cover}
\RequirePackage{tudelft-logo}

\IfPrintTF{
  \colorlet{chapternumbercolor}{black!50}
}{
  \colorlet{chapternumbercolor}{tud Blue!50}
}

% Load the TU Delft house style fonts: Roboto Slab for titles and Arial
% (sans-serif) for text. When using pdflatex, replace Arial by TeX Gyre Heros.
\if@fourier
  \RequirePackage[light]{roboto}
  \RequirePackage{tudelft-font-fourier}
  \newcommand{\headingfont}{\sffamily}
\else
  \RequirePackage{tudelft-font-roboto}
  \newcommand{\headingfont}{\robotoslab}
  \ifluatex%
    \IfFontExistsTF{Arial}{
      \newfontfamily{\arial}{Arial}
      \setsansfont[Scale=0.95]{Arial}
    }{
      \PackageError{\@currname}{The font Arial does not exist; please download it^^J
        from: https://www.freedesktop.org/software/fontconfig/webfonts}
    }
  \else
    \usepackage{tgheros}
    % since \slshape is undefined:
    \setkomafont{pageheadfoot}{\itshape}
  \fi
\fi

\addtokomafont{part}{\headingfont\color{accent}}
\addtokomafont{chapter}{\headingfont\color{accent}}
\addtokomafont{section}{\headingfont\color{accent}}

\setkomafont{chapterentry}{\bfseries}
\setkomafont{partentry}{\bfseries}

% Use roman (Georgia) in quote environment
\renewenvironment{quote}
  {\list{}{\rightmargin\leftmargin}\rmfamily\selectfont%
    \item\relax}
  {\endlist}

% Use TU Delft blue as the color for some details, unless the 'print' option is
% specified, in which case black is used instead.
\if@print
  \colorlet{accent}{black}
\else
  \colorlet{accent}{tud Blue}
\fi

% We use A4 paper with slightly smaller margins than the default (scale = 0.7).
\geometry{a4paper, hscale=0.75, vscale=0.8}

% Draw the line above a footnote in the accent color as well.
\renewcommand*\footnoterule{%
  \vspace*{-3pt}%
  {\color{accent}\hrule width 0.5\textwidth height 0.4pt}%
  \vspace*{2.6pt}%
}

\renewcommand\chapterlinesformat[3]{\Ifstr{#2}{}{}{#2\\[12pt]}#3}

\newcommand{\chapternumberfont}{%
  \fontsize{96pt}{96pt}%
  \if@fourier
    \bfseries
  \else
    \robotoslab\bfseries
  \fi
  \color{chapternumbercolor}\selectfont
}
\newcommand{\partnumberfont}{%
  \fontsize{96pt}{96pt}%
  \if@fourier
    \bfseries
  \else
    \robotoslab\bfseries
  \fi
  \color{chapternumbercolor}\selectfont
}


\RedeclareSectionCommands[
%  afterskip=.2\baselineskip,
%  tocentrynumberformat=\color{black},
]{part,chapter}

\renewcommand*{\raggedpart}{\raggedleft}
\renewcommand*{\raggedchapter}{\raggedleft}
\renewcommand*{\partformat}{{\chapternumberfont\thepart}\enskip}
\renewcommand*{\chapterformat}{{\chapternumberfont\thechapter}\enskip}

% ((Sub)sub)section titles start with the number in bold, followed by the name printed
% in the title color.
\if@fourier
  \renewcommand*{\sectionformat}{\textbf{\thesection.}\enskip}
  \renewcommand*{\subsectionformat}{\textbf{\thesubsection.}\enskip}
  \renewcommand*{\subsubsectionformat}{\textbf{\thesubsubsection.}\enskip}
\else
  \renewcommand*{\sectionformat}{\thesection.\enskip}
  \renewcommand*{\subsectionformat}{\thesubsection.\enskip}
  \renewcommand*{\subsubsectionformat}{\thesubsubsection.\enskip}
\fi


% Color the bullets of the itemize environment and make the symbol of the third
% level a diamond instead of an asterisk.
\renewcommand*\labelitemi{\color{accent}\textbullet}
\renewcommand*\labelitemii{\color{accent}--}
\renewcommand*\labelitemiii{\color{accent}$\diamond$}
\renewcommand*\labelitemiv{\color{accent}\textperiodcentered}

% don't color links for some commands
\newcommand{\hidelinksin}[1]{%
  \AddToHook{cmd/#1/before}{%
    \begingroup
    \unless\ifx\hypersetup\undefined
      \hypersetup{hidelinks}%
    \fi
  }%
  \AddToHook{cmd/#1/after}{\endgroup}
}

\hidelinksin{tableofcontents}
\hidelinksin{listoffigures}
\hidelinksin{listoftables}
