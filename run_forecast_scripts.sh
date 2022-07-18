#!/bin/bash
# Author: Ajda Savarin
# Created: July 16, 2020
# University of Washington
# asavarin@uw.edu
#
# This bash shell script will combine a bunch of steps (true/false switches) in creating the forecast template.
# Things you will need to change after downloading this to your computer:
#      - change true/false switches accoring to what you want executed
#      - if you do not have pdflatex installed, you will either need to install it, or change the compiler in $compile_latex
#
# Notes on true/false switches:
#      - for $compile_latex to run, you will need to have images, which are downloaded in $run_download
#      - for $rename_timestamp_templates to run, you will need the .pdf files produced by $compile_latex
#      - $clean_latex_tmpfiles will run regardless, but will only remove the latex auxilliary files if they are present (created by $compile_latex)

change_work_dir=true
run_archive=true
run_download=true
run_animations=true
run_processing=true
compile_latex=false
rename_timestamp_templates=false
clean_latex_tmpfiles=false

if $change_work_dir; then
  echo ""
  echo ""
  echo ""
  echo "... Changing working directory to CPEX forecast template."
  cd $PWD
fi

if $run_archive; then
  echo ""
  echo ""
  echo ""
  echo "... Archiving yesterday's imagery."
  python $PWD/supplementary/archive_yesterdays_images.py
fi

if $run_download; then
  echo ""
  echo ""
  echo ""
  echo "... Running download_daily_images_master.py"
  python $PWD/supplementary/download_daily_images_master.py
fi

if $run_animations; then
  echo ""
  echo ""
  echo ""
  echo "... Running create_animations.py"
  python ./supplementary/create_animations.py
fi

if $run_processing; then
  echo ""
  echo ""
  echo ""
  echo "... Running crop_edit_daily_images.py"
  python ./supplementary/crop_edit_daily_images.py
fi

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
  cp forecast_template_still.pdf ./forecast_files/CPEX-CV_Forecast_$(date +%Y-%m-%d)_still.pdf
  cp forecast_template_animated.pdf ./forecast_files/CPEX-CV_Forecast_$(date +%Y-%m-%d)_animated.pdf


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
