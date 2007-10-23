" Vim syntax file
" Language:     AsciiDoc
" Author:       Stuart Rackham <srackham@methods.co.nz> (inspired by Felix
"               Obenhuber's original asciidoc.vim script).
" Last Change:  AsciiDoc 8.2.0
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
syn match asciidocRuler /^'\{4,}$/
" The tricky part is not triggering on indented list items that are also
" preceeded by blank line, handles only bulleted items (see 'Limitations' above
" for workarounds).
syn region asciidocLiteralParagraph start=/^\n[ \t]\+\(\([^-*. \t] \)\|\(\S\S\)\)/ end=/\(^+\?\s*$\)\@=/
syn match asciidocListBullet /^\s*[-*+]\s/
syn match asciidocListNumber /^\s*\(\d*\.\{1,2}\|\l\?)\)\s\+/
syn match asciidocEmail /\S\+@\S\+\(.\S+\)*/
syn match asciidocAttributeRef /{\(\w\|-\)\+}/
syn match asciidocBlockTitle /^\.[^. \t].*[^-~_]$/
syn match asciidocAdmonition /^\u\{3,15}:\(\s\+.*\)\@=/
syn region asciidocSubscript start=/\~\S/ end=/\(\~\|^$\)/
syn region asciidocSuperscript start=/\^\S/ end=/\(\^\|^$\)/
syn region asciidocAttributeEntry start=/^:\a/ end=/:\(\s\|$\)/ oneline
syn region asciidocVLabel start=/^\s*/ end=/\S\(::\|;;\|:-\|??\)$/ oneline
syn region asciidocHLabel start=/^\s*/ end=/\S\(::\|;;\)\(\s\+\|\\$\)/ oneline
syn region asciidocMacroAttributes matchgroup=asciidocRefMacro start=/<<\w\(\w\|-\)*,\?/ end=/>>/
syn region asciidocMacroAttributes matchgroup=asciidocAnchorMacro start=/\[\{2}\(\w\|-\)\+,\?/ end=/\]\{2}/
syn region asciidocMacroAttributes matchgroup=asciidocAnchorMacro start=/\[\{3}\(\w\|-\)\+/ end=/\]\{3}/
syn region asciidocMacroAttributes matchgroup=asciidocMacro start=/\w\(\w\|-\)*:\S\{-}\[/ skip=/\\\]/ end=/\]/
syn region asciidocMacroAttributes matchgroup=asciidocIndexTerm start=/(\{2,3}/ end=/)\{2,3}/
syn match asciidocCommentLine "^//\([^/].*\|\)$" contains=asciidocToDo
" As a damage control measure quoted patterns always terminate at a  blank
" line (see 'Limitations' above).
syn region asciidocMonospaced start=/\(^\|[ \t(\[.,]\)\@<=+\([ )]\)\@!/ end=/\(+\([ \t)\],.?!;:]\|$\)\@=\|^$\)/
syn region asciidocMonospaced2 start=/\(^\|[ \t(\[.,]\)\@<=`\([ )]\)\@!/ end=/\(`\([ \t)\],.?!;:]\|$\)\@=\|^$\)/
syn region asciidocUnconstrainedMonospaced start=/++\S/ end=/\(++\|^$\)/
syn region asciidocEmphasized start=/\(^\|[ \t(\[.,]\)\@<=_\([ )]\)\@!/ end=/\(_\([ \t)\],.?!;:]\|$\)\@=\|^$\)/
syn region asciidocEmphasized2 start=/\(^\|[ \t(\[.,]\)\@<='\([ )]\)\@!/ end=/\('\([ \t)\],.?!;:]\|$\)\@=\|^$\)/
syn region asciidocUnconstrainedEmphasized start=/__\S/ end=/\(__\|^$\)/
syn region asciidocBold start=/\(^\|[ \t(\[.,]\)\@<=\*\([ )]\)\@!/ end=/\(\*\([ \t)\],.?!;:]\|$\)\@=\|^$\)/
syn region asciidocUnconstrainedBold start=/\*\*\S/ end=/\(\*\*\|^$\)/
syn region asciidocQuoted start=/\(^\|[ \t(\[.,]\)\@<=``\([ )]\)\@!/ end=/\(''\([ \t)\],.?!;:]\|$\)\@=\|^$\)/
syn region asciidocDoubleDollarPassthrough start=/\(^\|\W\)\@<=\$\{2,3}\S/ end=/\(\$\{2,3}\(\W\|$\)\@=\|^$\)/
syn region asciidocTriplePlusPassthrough start=/\(^\|\W\)\@<=+++\S/ end=/\(+++\(\W\|$\)\@=\|^$\)/
syn region asciidocTable start=/^\([`.']\d*[-~_]*\)\+[-~_]\+\d*$/ end=/^$/
syn match asciidocOneLineTitle /^=\{1,5}\s\+\S.*$/
syn match asciidocTwoLineTitle /^[^. +/].*[^.:]\n[-=~^+]\{2,}$/
syn match asciidocAttributeList /^\[[^[ \t].*\]$/
syn match asciidocQuoteBlockDelimiter /^_\{4,}$/
syn match asciidocExampleBlockDelimiter /^=\{4,}$/
syn match asciidocSidebarDelimiter /^*\{4,}$/
syn match asciidocListContinuation /^+$/
syn region asciidocLiteralBlock start=/^\.\{4,}$/ end=/^\.\{4,}$/ contains=asciidocCallout
syn region asciidocListingBlock start=/^-\{4,}$/ end=/^-\{4,}$/ contains=asciidocCallout
syn region asciidocCommentBlock start="^/\{4,}$" end="^/\{4,}$"
syn region asciidocPassthroughBlock start="^+\{4,}$" end="^+\{4,}$"
syn region asciidocFilterBlock start=/^\w\+\~\{4,}$/ end=/^\w\+\~\{4,}$/

highlight link asciidocMacroAttributes Label
highlight link asciidocIdMarker Special
highlight link asciidocDoubleDollarPassthrough Special
highlight link asciidocTriplePlusPassthrough Special
highlight link asciidocSubscript Type
highlight link asciidocSuperscript Type
highlight link asciidocOneLineTitle Title
highlight link asciidocTwoLineTitle Title
highlight link asciidocBlockTitle Title
highlight link asciidocRefMacro Macro
highlight link asciidocIndexTerm Macro
highlight link asciidocMacro Macro
highlight link asciidocAnchorMacro Macro 
highlight link asciidocEmail Macro
highlight link asciidocListBullet Label
highlight link asciidocListNumber Label
highlight link asciidocVLabel Label
highlight link asciidocHLabel Label
highlight link asciidocTable Type
highlight link asciidocListBlockDelimiter Label
highlight link asciidocListContinuation Label
highlight link asciidocLiteralParagraph Identifier
highlight link asciidocQuoteBlockDelimiter Type
highlight link asciidocExampleBlockDelimiter Type
highlight link asciidocSidebarDelimiter Type
highlight link asciidocLiteralBlock Identifier
highlight link asciidocListingBlock Identifier
highlight link asciidocPassthroughBlock Identifier
highlight link asciidocCommentBlock Comment
highlight link asciidocFilterBlock Type
highlight link asciidocBold Special
highlight link asciidocUnconstrainedBold Special
highlight link asciidocEmphasized Type
highlight link asciidocEmphasized2 Type
highlight link asciidocUnconstrainedEmphasized Type
highlight link asciidocMonospaced Identifier
highlight link asciidocMonospaced2 Identifier
highlight link asciidocUnconstrainedMonospaced Identifier
highlight link asciidocQuoted Label
highlight link asciidocToDo Todo
highlight link asciidocCommentLine Comment
highlight link asciidocAdmonition Special
highlight link asciidocAttributeRef Special
highlight link asciidocAttributeList Special
highlight link asciidocAttributeEntry Special
highlight link asciidocBackslash Special
highlight link asciidocCallout Label
highlight link asciidocLineBreak Special
highlight link asciidocRuler Type

let b:current_syntax = "asciidoc"

" vim: wrap et sw=2 sts=2:
