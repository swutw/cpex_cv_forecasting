#!/bin/bash
# Author: Ajda Savarin
# Created: July 16, 2020
# University of Washington
# asavarin@uw.edu
#

compile_latex=true
rename_timestamp_templates=false
clean_latex_tmpfiles=true

echo ""
echo ""
echo ""
echo "... Changing working directory to CPEX forecast template."
cd $PWD


echo ""
echo ""
echo ""
echo "... Running update_observed_imagery.py"
python $PWD/supplementary/update_observed_imagery.py


if $compile_latex; then
  echo ""
  echo ""
  echo ""
  echo "... Compiling the _still.tex template with pdfLatex"
  pdflatex --shell-escape --file-line-error forecast_template_still.tex
  pdflatex --shell-escape --file-line-error forecast_template_still.tex

  echo ""
  echo ""
  echo ""
  echo "... Compiling the _animated.tex template with pdfLatex"
  pdflatex --shell-escape --file-line-error forecast_template_animated.tex
  pdflatex --shell-escape --file-line-error forecast_template_animated.tex
fi

if $rename_timestamp_templates; then
  echo ""
  echo ""
  echo ""
  echo "... Renaming template files to CPEX format."
  cp forecast_template_still.pdf ./forecast_files/CPEX-AW_Forecast_$(date +%Y-%m-%d)_still.pdf
  cp forecast_template_animated.pdf ./forecast_files/CPEX-AW_Forecast_$(date +%Y-%m-%d)_animated.pdf


fi

if $clean_latex_tmpfiles; then
  echo ""
  echo ""
  echo ""
  echo "... Cleaning up LaTeX auxiliary files."
  for f in ./forecast_template_*aux; do
    echo "Removing $f"
    rm $f
  done
  
  for f in ./forecast_template_*log; do
    echo "Removing $f"
    rm $f
  done
  
  for f in ./forecast_template_*nav; do
    echo "Removing $f"
    rm $f
  done
  
  for f in ./forecast_template_*out; do
    echo "Removing $f"
    rm $f
  done
  
  for f in ./forecast_template_*snm; do
    echo "Removing $f"
    rm $f
  done
  
  for f in ./forecast_template_*toc; do
    echo "Removing $f"
    rm $f
  done
  
  for f in ./forecast_template_*pdf; do
    echo "Keeping $f"
  done
  
  for f in ./forecast_template_*tex; do
    echo "Keeping $f"
  done
fi

