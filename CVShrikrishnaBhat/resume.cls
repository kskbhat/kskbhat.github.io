%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Medium Length Professional CV
% LaTeX Class
% Version 4.0 (September 18, 2025)
%
% Copyright (C) 2010 by Trey Hunner
%
% Copying and distribution of this file, with or without modification,
% are permitted in any medium without royalty provided the copyright
% notice and this notice are preserved. This file is offered as-is,
% without any warranty.
%
% Created by Trey Hunner and modified by www.LaTeXTemplates.com
% Restructured and enhanced by Shrikrishna Bhat K
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
% CLASS DECLARATION AND BASE CLASS LOADING
%----------------------------------------------------------------------------------------
% Define the resume class and load base article class for general LaTeX support
\ProvidesClass{resume}[2025/09/18 v4.0 Resume class]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

%----------------------------------------------------------------------------------------
% CORE PACKAGES AND FONT SETUP
%----------------------------------------------------------------------------------------
% Basic formatting, layout, and font setup for elegant typography
\usepackage[parfill]{parskip}    % Removes paragraph indentation
\usepackage{array}               % Enhanced tabular column formatting
\RequirePackage{etoolbox}        % Logic tools (\ifthenelse, etc.)
\usepackage{graphicx}            % Image inclusion
\usepackage{tabularx}            % Flexible table widths
\usepackage{xstring}             % String operations
\usepackage{amsmath}             % Math formatting
\usepackage{xcolor}              % Color management
\usepackage{ebgaramond}          % EB Garamond professional font
\RequirePackage{microtype}       % Microtypography enhancements
\usepackage{ragged2e}            % Improved justification and ragged alignment

%----------------------------------------------------------------------------------------
% PAGE LAYOUT AND STYLE
%----------------------------------------------------------------------------------------
% Configure page margins and remove default headers/footers
\pagestyle{empty}
\usepackage{geometry}
\geometry{
	top=0.6in,
	bottom=0.6in,
	left=0.6in,
	right=0.6in,
}

%----------------------------------------------------------------------------------------
% ADDITIONAL PACKAGES FOR CV FEATURES
%----------------------------------------------------------------------------------------
% Extra formatting and interactivity tools
\usepackage{enumitem}           % Custom list spacing and bullets
\usepackage{fancyhdr}           % Custom headers and footers
\usepackage{lastpage}           % Page count reference
\usepackage[english]{babel}     % Language support
\usepackage{fontawesome7}       % Font Awesome v7 icons

% Enable long URLs with breaks
\usepackage{xurl}
\def\UrlBreaks{\do\/\do-}

% PDF metadata and link configuration
\usepackage[colorlinks=false, linkcolor=black, urlcolor=blue, citecolor=black,
pdfpagemode=UseNone, pdfstartview={FitH},
pdfcreator={github.com/kskbhat/resume · resume.cls v4.0 · LaTeX}]{hyperref}

%----------------------------------------------------------------------------------------
% DATE AND TIME UTILITIES
%----------------------------------------------------------------------------------------
% Handles formatted dates for CV entries or metadata
\usepackage[en-US]{datetime2}
\DTMusemodule{english}{en-US}
\DTMlangsetup[en-US]{showdayofmonth=false}
\DTMlangsetup[en-US]{abbr=true}

% Define date helper macros
\newcommand{\MonthYear}[2]{\DTMdate{#1-#2-01}}
\newcommand{\FullDate}[3]{%
	{\DTMlangsetup[en-US]{showdayofmonth=true}\DTMdate{#1-#2-#3}}%
}

% TodayFull → today's full date (e.g., "Oct 30, 2025")
\newcommand{\TodayFull}{%
	\DTMlangsetup[en-US]{showdayofmonth=true,abbr=true}%
	\DTMtoday%
}

%----------------------------------------------------------------------------------------
% INTERACTIVE AND CONDITIONAL CONTENT MODES
%----------------------------------------------------------------------------------------
% Adds conditional PDF-only/print-only content and attachment support
\usepackage{attachfile2}  % Embed file attachments in PDF
\usepackage{ocgx2}        % Optional content groups (hide/show)

% ---- Conditional Display Commands ----
% Visible in screen/PDF only
\newcommand{\screenonly}[1]{%
	\begin{ocg}[viewocg=always,printocg=never]{screen}{screen}{1}%
		#1%
	\end{ocg}%
}

% Visible in print only (hidden in PDF)
\newcommand{\printonly}[1]{%
	\begin{ocg}[viewocg=never,printocg=always]{print}{print}{1}%
		#1%
	\end{ocg}%
}

% ---- Conditional Logic Toggles ----
\newif\ifiref       % internal reference toggle
\newif\ifhide       % hide/show toggle
\newif\iflink       % hyperlink toggle

% Conditional reference or plain text
\newcommand{\iref}[2]{%
	\ifiref\href{#1}{#2}\else#2\fi
}

% Conditional hide/show environments
\newcommand{\hide}[1]{\ifhide\else #1\fi}
\newcommand{\revhide}[1]{\ifhide #1\fi}

% Conditional external links with icons
\newcommand{\extlink}[1]{%
	\iflink
	~\screenonly{\href{#1}{\tiny \faArrowUpRightFromSquare}}%
	\fi
}
\newcommand{\hlink}[2]{%
	\iflink
	\href{#1}{#2}%
	\fi
}

% --- Toggle for Cover Letter (new feature) ---
% Allows inclusion/exclusion of a cover letter in the CV document
\newif\ifcoverletter

% Command to conditionally print the cover letter
\newcommand{\coverletter}[1]{%
	\ifcoverletter
	% Only include if \coverlettertrue
	#1%
	\fi
}

\newcommand{\nocoverletter}[1]{%
	\ifcoverletter
	% do nothing
	\else
	#1%
	\fi
}

% --- Attachment toggles for PDF inclusion ---
\newif\ifattach
\newcommand{\pdflink}[1]{%
	\ifattach
	\smash{\attachfile[appearance=true,icon=Paperclip, scale = 0.3]{#1}{}}%
	\fi
}	
\newcommand{\filelink}[1]{%
	\smash{\attachfile[appearance=true,icon=Paperclip, scale = 0.3]{#1}{}}%
}
\newcommand{\filelinkifkeyword}[2]{%
	\ifkeyword{#1}{\filelink{#2}}{}%
}

% --- Attachment Note (screen-only) ---
\newcommand{\attachmentnote}{%
	\ifattach
	\vspace{0.5em}
	\screenonly{%
		{\begin{center}
			\footnotesize\color{gray!70}%
			\faCircleInfo\;Attachments open only in PDF readers that support embedded files (e.g., Adobe Acrobat Reader, Foxit PDF Reader). Click the \faPaperclip\;to view them.%
		\end{center}}%
	}
	\fi
}
%----------------------------------------------------------------------------------------
% HEADER AND FOOTER SETUP
%----------------------------------------------------------------------------------------
% Custom footer showing “Last Updated” date and page count
\newcommand{\setupheaderfooter}[2][]{%
	\pagestyle{fancy}%
	\fancyhf{}%
	\setcounter{page}{1}%
	\label{#2firstpage}%
	\fancyhead[R]{\color{lightgray}\tiny Last Updated: \today}%
	\fancyfoot[C]{\color{gray}\emph{#1~\textbullet~Page \thepage\ of \pageref{#2lastpage}}}%
	\renewcommand{\headrulewidth}{0pt}%
}

%----------------------------------------------------------------------------------------
% NAME, DEGREE, ADDRESS, PHOTO SETUP
%----------------------------------------------------------------------------------------
% Metadata commands for name, degree, address, and optional photo
\newcommand*{\name}[2]{%
	\def\givenname{#1}%
	\def\familyname{#2}%
	\def\fullname{#1\space #2}%
}
\newcommand{\degree}[1]{\def\@degree{#1}}
\def\@degree{}

% Define up to three address lines (with or without photo variants)
\newcommand{\addressSep}{\hspace{0.25cm}}
\let \@addressone \relax
\let \@addresstwo \relax
\let \@addressthree \relax

\newcommand{\address}[1]{
	\@ifundefined{@addressone}{
		\def \@addressone {#1}
	}{
		\@ifundefined{@addresstwo}{
			\def \@addresstwo {#1}
		}{
			\def \@addressthree {#1}
		}%
	}
}

% Photo-specific address variants
\let \@addressonewithphoto \relax
\let \@addresstwowithphoto \relax
\let \@addressthreewithphoto \relax

\newcommand{\addresswithphoto}[1]{
	\@ifundefined{@addressonewithphoto}{
		\def \@addressonewithphoto {#1}
	}{
		\@ifundefined{@addresstwowithphoto}{
			\def \@addresstwowithphoto {#1}
		}{
			\def \@addressthreewithphoto {#1}
		}%
	}
}

% Optional profile photo
\def\@photo{}
\def\@photosize{1.1in}
\newcommand{\photo}[2][1.1in]{%
	\def\@photosize{#1}%
	\def\@photo{#2}%
}

%----------------------------------------------------------------------------------------
% HEADER OUTPUT (NAME, ADDRESS, PHOTO)
%----------------------------------------------------------------------------------------
% Layout variations for resume title (with or without photo)
\newcommand{\printnameCenter}{
	\begingroup
	\hfil{\MakeUppercase{\huge{\bfseries\givenname} \familyname}\ {\space\small\@degree}}\hfil
	\bigskip\break
	\endgroup
}
\newcommand{\printnameLeft}{
	\begingroup
	\raggedright{\MakeUppercase{\huge{\bfseries\givenname} \familyname}\ {\space\small\@degree}}\par
	\bigskip
	\endgroup
}
\newcommand{\printaddressCenter}[1]{
	\begingroup
	\def \\ {\addressSep\ }%
	\centerline{#1}%
	\endgroup
	\par
	\smallskip
}
\newcommand{\printaddressLeft}[1]{%
	\begingroup
	\def \\ {\addressSep\ }%
	\raggedright #1\par
	\endgroup
	\smallskip
}

%----------------------------------------------------------------------------------------
% TITLE COMMANDS (MAIN DOCUMENT TITLE OUTPUT)
%----------------------------------------------------------------------------------------
% Resume title without photo
\newcommand{\resumetitle}{%
	\noindent
	\printnameCenter
	\@ifundefined{@addressone}{}{\printaddressCenter{\@addressone}}
	\@ifundefined{@addresstwo}{}{\printaddressCenter{\@addresstwo}}
	\@ifundefined{@addressthree}{}{\printaddressCenter{\@addressthree}}
	\par\vspace{0.25em}%
}

% Resume title with photo (aligned right)
\newcommand{\resumetitlewithphoto}{%
	\noindent
	\begin{minipage}[c]{0.72\textwidth}
		\printnameLeft
		\@ifundefined{@addressonewithphoto}{%
			\@ifundefined{@addressone}{}{\printaddressLeft{\@addressone}}%
		}{\printaddressLeft{\@addressonewithphoto}}%
		\@ifundefined{@addresstwowithphoto}{%
			\@ifundefined{@addresstwo}{}{\printaddressLeft{\@addresstwo}}%
		}{\printaddressLeft{\@addresstwowithphoto}}%
		\@ifundefined{@addressthreewithphoto}{%
			\@ifundefined{@addressthree}{}{\printaddressLeft{\@addressthree}}%
		}{\printaddressLeft{\@addressthreewithphoto}}%
	\end{minipage}%
	\hfill
	\begin{minipage}[c]{0.24\textwidth}
		\raggedleft
		\includegraphics[width=\@photosize]{\@photo}
	\end{minipage}%
	\par\vspace{0.25em}%
}

%----------------------------------------------------------------------------------------
% COUNTERS AND BOOKMARKING SETUP
%----------------------------------------------------------------------------------------
% Adds automatic PDF bookmarks for sections/subsections
\newcounter{rsection}
\newcounter{rsubsection}

%----------------------------------------------------------------------------------------
% MAIN CV SECTION ENVIRONMENTS
%----------------------------------------------------------------------------------------
% rSection: for major CV sections (e.g., Education, Experience)
\newenvironment{rSection}[2][]{%
	\stepcounter{rsection}%
	\pdfbookmark[1]{#2}{rsection.\thersection}%
	\medskip
	\MakeUppercase{\textbf{#2}}%
	\ifx\relax#1\relax\else\hspace{0em}#1\fi
	\medskip
	\hrule
}{}

%----------------------------------------------------------------------------------------
% SUBSECTION & ENTRY ENVIRONMENTS
%----------------------------------------------------------------------------------------
% rSubsection: used for job entries with title, date, and location
\newenvironment{rSubsection}[5][]{%
	\stepcounter{rsubsection}%
	\pdfbookmark[2]{#2}{rsubsection.\thersection.\thersubsection}%
	\textbf{#2}%
	\ifx\relax#1\relax\else\hspace{0em}#1\fi
	\hfill {#3}
	\ifthenelse{\equal{#4}{}}{}{%
		\\
		\emph{#4}\hfill \emph{#5}\\
		\vspace{-1.5em}
	} \par
}{}

% rSubsubsection: compact format for nested details
\newenvironment{rSubsubsection}[2]{%
	\vspace{-0.25em}
	\emph{#1}\hfill \emph{#2}\\
	\vspace{-1.5em}
	\par
}{}

% rSubheading: minimal variant for short entries
\newenvironment{rSubheading}[2][]{%
	\stepcounter{rsubsection}%
	\if\relax\detokenize{#2}\relax
	\else
	\pdfbookmark[2]{#2}{rsubheading.\thersection.\thersubsection}%
	\textbf{#2}%
	\ifx\relax#1\relax\else\hspace{0em}#1\fi
	\par
	\fi
}{}

%----------------------------------------------------------------------------------------
% LIST ENVIRONMENTS FOR COMPACT DISPLAY
%----------------------------------------------------------------------------------------
% rItemize and rEnumerate: compact bullet and numbered lists
\newenvironment{rItemize}{%
	\vspace{0.5em}
	\begin{list}{$\cdot$}{\leftmargin=1.25em}
		\setlength{\itemsep}{-0.5em} \vspace{-0.5em}
	}{%
	\end{list}
}
\newenvironment{rEnumerate}{%
	\vspace{0.5em}
	\begin{list}{\arabic{enumi}.}{\usecounter{enumi}\leftmargin=1.25em}
		\setlength{\itemsep}{-0.5em} 
		\vspace{-0.5em}
	}{%
	\end{list}
}

%----------------------------------------------------------------------------------------
% END OF CLASS FILE
%----------------------------------------------------------------------------------------
