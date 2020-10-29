# **Gillian Noonan**  &#x1F47B;&#x1F577;&#x1F578;&#x1F383;
## *Homework 9*
### 10/26/20
___

### Grade
3/3 - Nice work, I'm glad you feel like you learned something about APIs. It's totally fine if you remove your model for now.  You also wont use your model next week.

- Next time add your plot to the markdown :)

---
### Week 9 Questions
---
*1)A brief summary of the how you chose to generate your forecast this week.*
- I don't feel like the new time series made a positive improvement (or any change really) to my forecast yet, but the important thing is I learned quite a bit about APIs and spent quality time playing around with different sources - and.....it runs ;).  I did acquire a precipitation dataset that was only minorly useful to my analysis but provided a good test and trial dataset for learning how to work with API data and convert to time series.
- Seeing as how I have not been using my AR model all along I decided to remove it from the equation this week so as to simplify my learning base for the new topics.  I have a finite amount of time each week to spend coding and this week I primarily used that time towards reading through API and json introductory materials and training, playing with acquiring data from Mesonet and Daymet and seeing what i could do with it.  I was able to sign up for Mesonet and obtain data using their API and URL string for different "vars".  As well, I experimented with code in the training materials for acquiring info on nearby stations within an "x" mile radius of a lat/long point.  I was surprised to see that the starter code "stids" QVDA3 was not in the list(?).  I went through the starter code and looked at keys and types and tried to pull out data and that is where it got a bit challenging with the Mesonet dataset.  In the end, I think I did max out my token since I was getting HTTP 404 request errors or something of the sort.  Seeing as I was successful in downloading precip data from Daymet with no issues and seemed much more simplified dataset, I decided to move forward with that given the available time frame for work. I forecasted my model this week using what I have deemed "Jill's code".    

*2) A description of the dataset you added*

- I chose to ultimately use downloaded data from daymet - precipitation data.  It is in the form of "year", "yearday", and "precip".  I was able to figure out how to aggregate the data to weekly mean precipitation and do some plotting to visualize it.

*-What is the dataset?*

- The dataset is a dictionary with keys 'loc', 'Tile', 'Elevation', 'LCC', 'citation', and 'data'.  The key 'data' is also a dictionary with keys 'year', 'yday', 'day1 (s)', and 'prcp (mm/day)'.

*-Why did you choose it?*

- I chose it based on the fact that I wanted a precipitation dataset first of all.  Second of all, I played around with Mesonet for a while and found it more challenging so decided to go with daymet for final code since it was less of a mess.  Deleted my work with mesonet for clean code file.  Upon finding that daymet data for our pixel only goes up to 12/31/19, I realized that this source will not be super useful for near-term analysis, but did not have time to go look for additional source and repeat the process before assignment due date.

*-What location have you chosen?*

I used the precise lat/long pixel to pull out data for the same pixel as the USGS stream gauge location.

*-Where did you get the data from?*

- I got the data from daymet - entered lat/long for our pixel, selected precip dataset and copied the url.

*-What was your approach to accessing it?*

- I used the url method in my code to pull the data from daymet in json format, then converted to pandas dataframe to work with as time series.

*3) A plot of your additional time series along with your streamflow time series.*

- I was able to plot this data separately, but not able to figure out yet a combined plot, though I have tried.  Intention was to add historical weekly mean precip to my weekly historical min flow plots.   Not that this adds much to my forecast, but more so as an exercise in just figuring out how to do it!  Also, I would have tried adding the last two weeks of precip to my 'two-week trend' plot, but the daymet data only goes through 12/31/19!
---

&#x1F600;
**Thanks!**  
