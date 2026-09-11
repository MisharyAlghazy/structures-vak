#! /usr/bin/env bash
sed '/## Fonts/,$d; 1,2d' README.md | pandoc -o description-Overleaf.html
sed -i '/## Installing the template/,$d' README.md
echo "
## Version management on Gitlab

The source files can be found on [Gitlab](${CI_PROJECT_URL}).
It is designed to work with LuaLaTeX and PdfLaTeX (faster but less features and less fancy font support).
On the Gitlab site more information can be found on using LaTeX and this template outside of Overleaf.

This version was created from Git commit $(git rev-parse --short HEAD) on $(date -I).
" >> README.md
