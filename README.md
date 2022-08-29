# cpex-cv_forecasting

Forecasting template and tools for creating daily weather forecasts for the CPEX-CV field experiment.

To run the scripts in this directory, you will need to following:

1. ImageMagick (for image processing).
2. Python v3.x (I use 3.7.4) with following modules:
    - bs4 (HTML parsing; if python yells at you about "Couldn't find a tree builder ", you may have to conda/pip install lxml)
    - datetime (dealing with dates)
    - numpy (number stuff)
    - Image (Create gif files)
    - os (reading existing files)
    - subprocess (executing code outside python)
    - urllib (retrieving images)
    - time
3. Microsoft Powerpoint.


Google Drive document with links and resources: https://docs.google.com/document/d/1fbgHyg7smXdD6AVZyczOzl1UvFjeB5TxeZdQ1_8xoxE/edit?usp=sharing

Google Drive slides for forecasting template: https://docs.google.com/presentation/d/1v5T9YzH2UPFGwBxoqUROgIJYlRP-EVWW/edit?usp=sharing&ouid=113115779828168659760&rtpof=true&sd=true


-------------------------------------------
# Steps for automatically downloading the figures

(This won't work unless your manual steps work.)
 - Before you run them for the first time, you will need to make the files executable (on Mac/Linux: chmod +x run_forecast_scripts.sh)

1. **python ./run_forecast_scripts.py** will run all the steps in the manual section **BUT**

 - You will need to open it up and edit a few things (instructions at the top of the .sh file)
    - Decide on steps you need to run for true/false switches.
    - Change true/false _switched_download.txt_ according to what you want to download

-------------------------------------------
# Steps for manually downloading the figures

These should be run from the main directory.

1. Archive previous day's images: **python ./supplementary/archive_yesterdays_images.py**

This will take all the images from _./figs_final/_ and move them into a new directory, if they are not already saved.
It will then remove all the images from -./figs/_, _./figs_cropped/_, and _./figs_final/_.

2. Download updated images for the forecast: **python ./supplementary/download_daily_images_master.py**

This will:
    - download images for the forecasting template. As long as not all images are available (i.e. some links did not work the first time), it will only download the missing images. If all images are present, it will re-download everything to update images to the last available time.
    - reports on status of images (e.g. tells you if they are not available).
    - saves all the available images in the _./figs/_ directory.

3. Create basic animations: **python ./supplementary/create_animations.py**

This will:
    - extend the last frame of each future animations by 3 frames, so a looping animation will stay longer at the last frame.

4. Crop, process, and annotate downloaded images: **python ./supplementary/crop_edit_daily_images.py**

This reads in _switches_process.txt_ that was created in 2. It's automatic, so no need for any changes. It:
    - adds the locations of Sal wherever applicable.
    - crops images.
    - joins images together for animations.
    - creates final animations.
    - puts all intermediate imagery to _./figs_cropped/_.
    - puts all final imagery (for the .pptx template) to _./figs_final/_.


-------------------------------------------
# Steps for creating the Microsoft PowerPoint template
Make sure you have downloaded image files and cropped them before starting this.

1. Copy the forecast_template_link.pptx file and rename it. Then open the new file.

When you first open it, this will include a lot of messages that a specific image was not found. Proceed to step 2 (only needs to be done once after you download everything), but only after you've gone through the ./run_forecast_scripts.sh to have all the images downloaded and processed. (Or run the maual steps 1-4 from above, in that order).

2. You will need to set the links working on your personal computer. This might vary from machine to machine, or from one PowerPoint version to another. But in general, here's what you need to do **for each image in the template**:
- Click on the image and open the **Format picture** panel (Picture Format in top menu var, then Format Pane).
- Under **Shape Options**, click on **Fill and Line** tab (the one that looks like a paint bucket).
- Under the **Fill section**, make sure *Picture or texture fill* is chosen, and click on the **Insert ...**. button under *Picture source*. This will open a window where you can search for the image you want to link to.
- Find the image you want to link (there's a list in _ppt_linked_images.txt_) and highlight it. All images for the ppt are stored in **/figs_final/**.
- Click on the **Options** button in the bottom left corner (this might vary), and tick both the **Link to File**, and the **Save with Document** boxes.
- Click **Insert**.

As you add each new link, the empty figure should be replaced with what it is being linked to. As you go through the file, you will see the file size increase (from <500KB to >60MB).

**Preparing a forecast**

3. After downloading and processing new images (daily), open the forecast template PowerPoint file and check that the images have updated. For example, model images have a timestamp on the top right, you can check over there. Also compare with individual images in the _./figs_final/_ directory.

4. Go through and manually update all the dates that appear in titles. The dates in the footer (bottom left corner) will update automatically.

5. Annotate the document with comments, highlights, summaries, etc.

6. Copy (or Duplicate) the finished PPT file, and name it following this example: **CPEX-CV_Forecast_YYYY-MM-DD.pptx**

7. Move the final document to Google Drive.
