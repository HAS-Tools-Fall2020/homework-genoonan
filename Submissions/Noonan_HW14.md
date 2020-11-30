# **Gillian Noonan**  &#x1F604;
## *Homework 14*
### 11/30/20
___

### Grade


---
### Week 14 Questions
---
*1) What is the paper or project you picked? Include a title, a link the the paper and a 1-2 sentence summary of what its about.*
- I spent a decent amount of time first of all trying to find a paper with 1) an associated github python-related repo, and 2) one that looked useful and interesting.   I did some rogue googling to start, looking for geotechnical/hydrogeology/hydrology python papers and came across some interesting things but none useful for this task.   Then I went to Nature.com and started poking around there and found one with a really good looking readme so went with that.

  - Title:  "*Towards learning universal, regional, and local hydrological behaviors via machine learning applied to large-sample datasets*"
  - Link: https://arxiv.org/pdf/1907.08456v2.pdf

  - What it is about:
    - This paper exhibits improved regional rainfall-runoff modeling using a novel, data-driven approach using Long ShortTerm Memory networks (LSTMs). By training a single LSTM model on 531 basins from the CAMELS data set using meteorological time series data and static catchment attributes, the authors were able to significantly improve performance compared to a set of several different hydrological benchmark models. The authors approach not only significantly outperforms hydrological models that were calibrated regionally but also achieves better performance than hydrological models that were calibrated for each basin individually.

*2) What codes and/or data are associated with this paper? Provide any link to the codes and datasets and a 1-2 sentence summary of what was included with the paper (i.e. was it a github repo? A python package? A database? Where was it stored and how?)*
- The paper included a link to a github repo.  Github link: https://github.com/kratzert/ealstm_regional_modeling
- Data to download include:
  - CAMELS data sets (download here: https://ral.ucar.edu/solutions/products/camels):
    - CAMELS time series meteorology, observed flow, meta data (.zip) (very large dataset - was going to take 2 hours to extract the zip file so i gave up on recreating the paper results at this point since it specifically states in the readme "First of all you need the CAMELS data set, to run any of your code")
    - CAMELS Attributes (.zip)
  - updated version of the Maurer forcing data (download here from Hydroshare: https://www.hydroshare.org/resource/17c896843cf940339c3c3496d0c1c077/)
  - CAMELS benchmark models (download here from Hydroshare: https://www.hydroshare.org/resource/474ecc37e7db45baa425cdb4fc1b61e1/)
    - This one is a netcdf.tar.xz (also accompanied by a very organized-looking readme)

*3) Summarize your experience trying to understand the repo:*  
- *Was their readme helpful? How was their organization?*  
  - Their readme was so helpful and their repo was organized - even providing copy-and-paste terminal commands to clone the repo, and set up an environment with all needed packages (using a .yml file).  HOWEVER, it failed to run on my computer "$ conda env create -f environment_cpu.yml, Collecting package metadata (repodata.json): ...working... done
Solving environment: ...working... failed".


- *What about documentation within the code itself?*
 - I peeked at a couple of .py files still and they also look well commented.  But they just look like they are full of functions!  Seriously, everything is a function and i wonder if this is normal organization for complex code.  I like the headers they put in the main.py that look like this and appear to define all of their million functions by section:

      "#############  
      ""# Prepare run #  
      ""############

      Interestingly the model evaluation commands were all run through terminal using python commands.  "python main.py ....." (example: python main.py evaluate --camels_root /path/to/CAMELS --run_dir path/to/model_run)
      Just not something we've done (i think) or that i don't do.  So used to running in VSCode that this seemed strange, but also very concise!  

*4) Summarize your experience trying to work with their repo: What happened? Where you successful? Why or why not?*
- I was easily able to clone their repo and find all of the data needed.  I was hung up on trying to run the terminal command provided to set up an environment with all needed packages.  But even before that, i gave up when the amount of data to be downloaded and extracted exceeded BY FAR the time limit on this assignment.

*5) Summarize your experience working with the data associated with this research. Could you access the data? Where was it? Did it have a DOI? What format was it in?*
- The data was all linked and explained well (including specific file/folder names and where to extract and download to so code would run).  Some was available for direct download from NCAR Research Applications Laboratory (CAMELS (Catchment Attributes and Meteorology for Large-sample Studies)), while others were posted on Hydroshare by the authors.

*6) Did this experience teach you anything about your own repo or projects? Things you might start or stop doing?*
- Detail, detail, detail.  Make no assumptions that the person trying to use it knows anything about anything at all ha.  I really like the concise setup of just copy and paste commands to get everything all set up nice and tidy with the cloned repo and the environment.  Also, sort of learned what is a "pickle file"??? [converts python objects to character stream to save on disk] - (where results were ultimately stored in this modeling).  Also sort of learned the difference in a CPU and a GPU....

  Overall, i enjoyed this assignment and thought it was a good learning experience to see what was out there, how to find it, and how to TRY to use it.  And was impressed with myself that i could get at least some of the way to recreating and understanding what was going on.  Much more so than where I existed back in August before this class!  Very useful.   

---

&#x1F600;
**Thanks!**  
