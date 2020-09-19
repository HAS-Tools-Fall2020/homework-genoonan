# **Gillian Noonan**
## *Homework 3*
### 9/14/20

---------
# Grade

3/3 - Nice work! You are doing it right. Right now we are really writing python codes that are exploratory. Its up to you how you want to use this data exploration to guide your forecasts. And you are correct for the long term forecast you can only use the data up to August 21st. So you could update it if you felt with your analysis you had a better sense of the weekly paternns but you don't have to.

One note: on question 1 the flow data is a 'float' and the others are integers


---
### Week 3 Questions
---
**1) Describe the variables flow, year, month, and day.   What type of objects are they, what are they composed of, and how long are they?**

**Answer:** Flow, year, month and day are lists.  Flow is a float object.  Year, month and day are integers.  The lists are all 11578 records long.

**2) How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?**

**Answer:** My one week forecast for Week 3 (average flow for 9/13-9/19) was 60.  Using the for loop in the starter code, and considering all months of September since 1989, the number of times for the month of September the flow was greater than 60 is 893.  A count on how many flow rates there are when month = 9, gives me a (len) of 942.  Calculating the percentage in the code for these two variables gives 94.8% of times it has been higher than my forecast in September.  

**3) How would your answer to the previous question change if you considered only daily flows in or before 2000?  Same question for the flows in or after the year 2010? (again report toal number of times and percentage)**

**Answer:**  For in or prior to 2000, the total times the flow was greater than 60 is 360 times, or 100% of daily flows for September at years less than 2000 were greater than my prediction.  For in or greater than 2010, there were 285 instances in the month of September where flow was greater than 60.  There were 312 September recordings since 2010, which equates to 91.3% greater readings than my prediction.

**4) How does the daily flow generally change from the first half of September to the second?**

**Answer:** The mean flow for the beginning of September (day<16) is 178.8.   The mean flow for the end of September (day>=16) is 169.8.  Therefore, the daily flow generally reduces in the second half of September.  Note: I also attempted to produce some plots but had no success in isolating September data or by day - though i did play around for a while trying to figure out. I left this in the code in case you have any suggestions.

**Week 3 Forecast Rationale**
---
For Week 3 forecast, I just updated the one week and two-week forecast a bit based on what the current data are showing.  And mostly just spent most of my effort on trying to figure out the Python coding part to answer the homework questions.  I didn't see any reason to update the seasonal forecast I made using excel at this point(?), so I left all the same as forecasted last week.  Or maybe I'm just not understanding how that is supposed to work.  Or maybe i need to work more on figuring out some code to help me out.  I recall you saying something about not using data from the actual gauge report to fill in weeks that have passed in our seasonal list so I assume we would just leave those values as is as we go along though??

**Thanks!**  
