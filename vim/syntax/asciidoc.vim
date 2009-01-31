" Vim syntax file
" Language:     AsciiDoc
" Author:       Stuart Rackham <srackham@gmail.com> (inspired by Felix
"               Obenhuber's original asciidoc.vim script).
" URL:          http://www.methods.co.nz/asciidoc/
" Licence:      GPL (http://www.gnu.org)
" Remarks:      Vim 6 or greater
" Limitations:  See 'Appendix J: Vim Syntax Highlighter' in the AsciiDoc 'User
"               Guide'.

if exists("b:current_syntax")
  finish
endif

syn clear
syn sync fromstart
syn sync linebreaks=1

" Run :help syn-priority to review syntax matching priority.
syn keyword asciidocToDo TODO FIXME XXX ZZZ
syn match asciidocBackslash /\\/
syn region asciidocIdMarker start=/^\$Id:\s/ end=/\s\$$/
syn match asciidocCallout /\\\@<!<\d\{1,2}>/
syn match asciidocListBlockDelimiter /^--$/
syn match asciidocLineBreak /[ \t]+$/
syn match asciidocRuler /^'\{3,}$/
syn match asciidocPagebreak /^<\{3,}$/
syn match asciidocEntityRef /\\\@<!&[#a-zA-Z]\S\{-};/
" The tricky part is not triggering on indented list items that are also
" preceeded by blank line, handles only bulleted items (see 'Limitations' above
" for workarounds).
syn region asciidocLiteralParagraph start=/^\n[ \t]\+\(\([^-*. \t] \)\|\(\S\S\)\)/ end=/\(^+\?\s*$\)\@=/
syn match asciidocURL /\\\@<!\<\(http\|https\|ftp\|file\|irc\):\/\/[^| \t]*\(\w\|\/\)/
syn match asciidocEmail /\\\@<!\(\<\|<\)\w\(\w\|[.-]\)*@\(\w\|[.-]\)*\w>\?[0-9A-Za-z_.]\@!/
syn match asciidocAttributeRef /\\\@<!{\w\(\w\|-\)*\([=!@#$%?:].*\)\?}/
syn match asciidocAdmonition /^\u\{3,15}:\(\s\+.*\)\@=/

" As a damage control measure quoted patterns always terminate at a  blank
" line (see 'Limitations' above).
syn match asciidocQuotedSubscript /\\\@<!\~\S\_.\{-}\(\~\|\n\s*\n\)/
syn match asciidocQuotedSuperscript /\\\@<!\^\S\_.\{-}\(\^\|\n\s*\n\)/
syn match asciidocQuotedMonospaced /\(^\|[| \t([.,=]\)\@<=+\([ )\n]\)\@!\_.\{-}\S\(+\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
syn match asciidocQuotedMonospaced2 /\(^\|[| \t([.,=]\)\@<=`\([ )\n]\)\@!\_.\{-}\S\(`\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
syn match asciidocQuotedUnconstrainedMonospaced /\\\@<!++\S\_.\{-}\(++\|\n\s*\n\)/
syn match asciidocQuotedEmphasized /\(^\|[| \t([.,=]\)\@<=_\([ )\n]\)\@!\_.\{-}\S\(_\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
syn match asciidocQuotedEmphasized2 /\(^\|[| \t([.,=]\)\@<='\([ )\n]\)\@!\_.\{-}\S\('\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
syn match asciidocQuotedUnconstrainedEmphasized /\\\@<!__\S\_.\{-}\(__\|\n\s*\n\)/
syn match asciidocQuotedBold /\(^\|[| \t([.,=]\)\@<=\*\([ )\n]\)\@!\_.\{-}\S\(\*\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
syn match asciidocQuotedUnconstrainedBold /\\\@<!\*\*\S\_.\{-}\(\*\*\|\n\s*\n\)/
"syn match asciidocQuotedSingleQuoted /\(^\|[| \t([.,=]\)\@<=`\([ )\n]\)\@!\_.\{-}\S\('\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
" Don't allow ` in single quoted (a kludge to stop confusion with `monospaced`).
syn match asciidocQuotedSingleQuoted /\(^\|[| \t([.,=]\)\@<=`\([ )\n]\)\@!\([^`]\|\n\)\{-}[^`\s]\('\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/
syn match asciidocQuotedDoubleQuoted /\(^\|[| \t([.,=]\)\@<=``\([ )\n]\)\@!\_.\{-}\S\(''\([| \t)[\],.?!;:=]\|$\)\@=\|\n\s*\n\)/

syn match asciidocDoubleDollarPassthrough /\\\@<!\(^\|[^0-9a-zA-Z$]\)\@<=\$\$..\{-}\(\$\$\([^0-9a-zA-Z$]\|$\)\@=\|^$\)/
syn match asciidocTriplePlusPassthrough /\\\@<!\(^\|[^0-9a-zA-Z$]\)\@<=+++..\{-}\(+++\([^0-9a-zA-Z$]\|$\)\@=\|^$\)/

syn match asciidocListBullet /^\s*\zs\(-\|\*\{1,5}\)\ze\s/
syn match asciidocListNumber /^\s*\zs\(\(\d\+\.\)\|\.\{1,5}\|\(\a\.\)\|\([ivxIVX]\+)\)\)\ze\s\+/

syn region asciidocTable_OLD start=/^\([`.']\d*[-~_]*\)\+[-~_]\+\d*$/ end=/^$/
syn match asciidocBlockTitle /^\.[^. \t].*[^-~_]$/ contains=asciidocQuoted.*,asciidocAttributeRef
syn match asciidocOneLineTitle /^=\{1,5}\s\+\S.*$/ contains=asciidocQuoted.*,asciidocAttributeRef

syn match asciidocTitleUnderline /[-=~^+]\{2,}$/ transparent contained contains=NONE
syn match asciidocTwoLineTitle /^[^. +/].*[^.:]\n[-=~^+]\{2,}$/ contains=asciidocQuoted.*,asciidocAttributeRef,asciidocTitleUnderline

syn match asciidocAttributeList /^\[[^[ \t].*\]$/
syn match asciidocQuoteBlockDelimiter /^_\{4,}$/
syn match asciidocExampleBlockDelimiter /^=\{4,}$/
syn match asciidocSidebarDelimiter /^*\{4,}$/

"See http://vimdoc.sourceforge.net/htmldoc/usr_44.html for excluding region
"contents from highlighting.
syn match asciidocTablePrefix /\(\d\+\*\)\?|/ containedin=asciidocTableBlock contained
syn region asciidocTableBlock matchgroup=asciidocTableDelimiter start=/^|=\{3,}$/ end=/^|=\{3,}$/ keepend contains=ALL
syn match asciidocTablePrefix2 /\(\d\+\*\)\?!/ containedin=asciidocTableBlock2 contained
syn region asciidocTableBlock2 matchgroup=asciidocTableDelimiter2 start=/^!=\{3,}$/ end=/^!=\{3,}$/ keepend contains=ALL

syn match asciidocListContinuation /^+$/
syn region asciidocLiteralBlock start=/^\.\{4,}$/ end=/^\.\{4,}$/ contains=asciidocCallout keepend
syn region asciidocOpenBlock start=/^-\{4,}$/ end=/^-\{4,}$/ contains=asciidocCallout keepend
syn region asciidocCommentBlock start="^/\{4,}$" end="^/\{4,}$" contains=asciidocToDo
syn region asciidocPassthroughBlock start="^+\{4,}$" end="^+\{4,}$"
" Allowing leading \w characters in the filter delimiter is to accomodate
" the pre version 8.2.7 syntax and may be removed in future releases.
syn region asciidocFilterBlock start=/^\w*\~\{4,}$/ end=/^\w*\~\{4,}$/

syn region asciidocMacroAttributes matchgroup=asciidocRefMacro start=/\\\@<!<<"\{-}\w\(\w\|-\)*"\?,\?/ end=/\(>>\)\|^$/ contains=asciidocQuoted.* keepend
syn region asciidocMacroAttributes matchgroup=asciidocAnchorMacro start=/\\\@<!\[\{2}\(\w\|-\)\+,\?/ end=/\]\{2}/ keepend
syn region asciidocMacroAttributes matchgroup=asciidocAnchorMacro start=/\\\@<!\[\{3}\(\w\|-\)\+/ end=/\]\{3}/ keepend
syn region asciidocMacroAttributes matchgroup=asciidocMacro start=/[\\0-9a-zA-Z]\@<!\w\(\w\|-\)*:\S\{-}\[/ skip=/\\\]/ end=/\]\|^$/ contains=asciidocQuoted.* keepend
syn region asciidocMacroAttributes matchgroup=asciidocIndexTerm start=/\\\@<!(\{2,3}/ end=/)\{2,3}/ contains=asciidocQuoted.* keepend
syn region asciidocMacroAttributes matchgroup=asciidocAttributeMacro start=/\({\(\w\|-\)\+}\)\@<=\[/ skip=/\\\]/ end=/\]/ keepend

syn match asciidocCommentLine "^//\([^/].*\|\)$" contains=asciidocToDo

syn region asciidocVLabel start=/^\s*/ end=/\(::\|;;\)$/ oneline contains=asciidocQuoted.*,asciidocMacroAttributes keepend
syn region asciidocHLabel start=/^\s*/ end=/\(::\|;;\)\(\s\+\|\\$\)/ oneline contains=asciidocQuoted.*,asciidocMacroAttributes keepend

syn region asciidocAttributeEntry start=/^:\w/ end=/:\(\s\|$\)/ oneline

highlight link asciidocMacroAttributes Label
highlight link asciidocIdMarker Special
highlight link asciidocDoubleDollarPassthrough Special
highlight link asciidocTriplePlusPassthrough Special
highlight link asciidocQuotedSubscript Type
highlight link asciidocQuotedSuperscript Type
highlight link asciidocOneLineTitle Title
highlight link asciidocTwoLineTitle Title
highlight link asciidocBlockTitle Title
highlight link asciidocRefMacro Macro
highlight link asciidocIndexTerm Macro
highlight link asciidocMacro Macro
highlight link asciidocAttributeMacro Macro
highlight link asciidocAnchorMacro Macro 
highlight link asciidocEmail Macro
highlight link asciidocListBullet Label
highlight link asciidocListNumber Label
highlight link asciidocVLabel Label
highlight link asciidocHLabel Label
highlight link asciidocTable_OLD Type
highlight link asciidocTableDelimiter Label
highlight link asciidocTableBlock NONE
highlight link asciidocTablePrefix Label
highlight link asciidocTableDelimiter2 Label
highlight link asciidocTableBlock2 NONE
highlight link asciidocTablePrefix2 Label
highlight link asciidocListBlockDelimiter Label
highlight link asciidocListContinuation Label
highlight link asciidocLiteralParagraph Identifier
highlight link asciidocQuoteBlockDelimiter Type
highlight link asciidocExampleBlockDelimiter Type
highlight link asciidocSidebarDelimiter Type
highlight link asciidocLiteralBlock Identifier
highlight link asciidocOpenBlock Identifier
highlight link asciidocPassthroughBlock Identifier
highlight link asciidocCommentBlock Comment
highlight link asciidocFilterBlock Type
highlight link asciidocQuotedBold Special
highlight link asciidocQuotedUnconstrainedBold Special
highlight link asciidocQuotedEmphasized Type
highlight link asciidocQuotedEmphasized2 Type
highlight link asciidocQuotedUnconstrainedEmphasized Type
highlight link asciidocQuotedMonospaced Identifier
highlight link asciidocQuotedMonospaced2 Identifier
highlight link asciidocQuotedUnconstrainedMonospaced Identifier
highlight link asciidocQuotedSingleQuoted Label
highlight link asciidocQuotedDoubleQuoted Label
highlight link asciidocToDo Todo
highlight link asciidocCommentLine Comment
highlight link asciidocAdmonition Special
highlight link asciidocAttributeRef Special
highlight link asciidocAttributeList Special
highlight link asciidocAttributeEntry Special
highlight link asciidocBackslash Special
highlight link asciidocEntityRef Special
highlight link asciidocCallout Label
highlight link asciidocLineBreak Special
highlight link asciidocRuler Type
highlight link asciidocPagebreak Type
highlight link asciidocURL Macro

let b:current_syntax = "asciidoc"

" vim: wrap et sw=2 sts=2:
