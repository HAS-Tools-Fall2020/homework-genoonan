# **Gillian Noonan**
## *Homework 4*
### 9/21/20

---------

### Week 4 Questions
---
**1) Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.**

 - Discussion for my one-week prediction (9/20-9/26):
    - To start i just wanted to see how flow data for September compared with all data, and how has changed over time (and play around with histograms a bit):
     - For histograms:
        - I looked at all flow data (as provided in the starter code), then isolated just September for all data
        - I then looked at September for just the last 10 years
        - I then plotted just September for the last 2 years.  
        - I then looked at just September for last 10 years and last 2 years for specific data in the week of 9/20 - 9/26 (our one-week forecast dates).   For this week the last 2 years, I saw that the majority of the data fell below 160cfs for September.  
        - I then looked at histogram for just September of 2020 and see the range of flows has only been from approximately 35 to 71cfs which is much lower.  (side note: i need to work on better naming convention b/c they are getting a little long i think)
     - For flow quantiles:
        - To find recent trends, I looked at September 2020 quantiles for 0, 0.25, 0.5, and 0.75 which were 36.6, 45.2, 52.35, and 57.475.  The min, max, mean and median were 36.6, 65.3, 51.3, and 52.3.

- Discussion for my two-week prediction (9/27-10/3):
  - This one is a bit harder to isolate because it spans two months with same contained days.  I was unsuccessful with this code using an 'or' statement but Laura debugged and I learned that the 'or' statement will not work with numpy - need to instead use the '|' symbol in its place and then it runs.
    - For histograms:  
      - I looked at early October (days 1-3) for last 10 years and found the flow ranged up to near 500cfs but primarily was approximately 75-175cfs over last 10 years - still much higher than my prediction.  
      - I looked at 9/27 - 9/30 and 10/1 - 10/3 for last 2 years and it was similar, primarily in the 50-300 range, with minimal occurrence greater than 400cfs.
      - I then looked at all of October histogram for year 2019.  Range appears to be primarily within approx. 65-115cfs range.  
    - For quantiles:  
        - I looked at quantiles and stats for early October for last 10 years (Oct 1-3).  Quantiles for 0, 0.25, 0.5, and 0.75 were 71.7, 82.175, 93.45, and 132.25.  The min, max, mean and median were 71.7, 433, 120.5, and 93.5.  All much higher than my current forecast!
        - I looked at quantiles and stats for 9/27 - 10/3 for last 2 years.  Quantiles for 0, 0.25, 0.5, and 0.75 were [71.3  88.6 108.  134. ].  The min, max, mean and median were 71.3, 433.0, 121.45841584158417, and 108.0.
        - I also looked at quantiles and stats for October of 2019.  Quantiles for 0, 0.25, 0.5, and 0.75 were 72.7, 80.55, 88.7, and 93.95.  The min, max, mean and median were 72.7, 111, 87.7, and 88.7.  Still all much higher than my current forecast but as you said, the word "mega-drought" is being thrown about!  

**2) Describe the variable flow_data:**

  - *What is it?*  
     - flow_data is an N-dimensional numpy array (numpy.ndarray)


  - *What type of values is it composed of?*  
      - float64.  Column 0 is year, column 1 is month, column 2 is day, column 3 is flow rate.


  - *What are its dimensions, and total size?*
    - Flow_data is two-dimensional (2) array and shape is (11584, 4) which means 11584 rows and 4 columns.


**3) How many times was the daily flow greater than your prediction in the month of September (express your answer in terms of the total number of times and as a percentage)?**

- Answer: Flow was greater than my prediction 915 times.  There are 948 total values recorded for September so the percentage of times greater is 96.5%!


**4) How would your answer to the previous question change if you considered only daily flows in or before 2000? Same question for the flows in or after the year 2010? (again report total number of times and percentage)**

- Answer:
  - In or before 2000: Flow was greater than my prediction 360 times.  Total September data values in or before 2000 is 360, so 100%!
  - In or after 2010: Flow was greater than my prediction 299 times.  Total September data values in or before 2000 is 318, so 94%!


**5) How does the daily flow generally change from the first half of September to the second?**

- Answer: The daily flow generally decreases in September based on the average of 1st half of September over the data period = 178.1 and the average over the last half of September =  169.1



---


**Thanks!**  
