# **Gillian Noonan**
## *Homework 4*
### 9/21/20

---------

### Week 4 Questions
---
**1) Include discussion of the quantitative analysis that lead to your prediction. This can include any analysis you complete but must include at least two histograms and some quantitative discussion of flow quantiles that helped you make your decision.**

 - Discussion for my one-week prediction:
  - To start i wanted to see how flow data for September compared with all data, and how has changed over time:
     - For histograms, i looked at all flow data (as provided in the starter code), then isolated just September for all data, then looked at September for just the last 10 years, then just September for the last 2 years.  I then looked at just September for last 10 years and last 2 years for specific data in the week of 9/20 - 9/26 (our one-week forecast dates).   For this week the last 2 years, I saw that the majority of the data fell below 160cfs for September.  I then looked at histogram for just September of 2020 and see the range of flows has only been from approximately 35 to 71cfs which is much lower.  
     - For flow quantiles, to find recent trends, I looked at September quantiles for 0, 0.25, 0.5, and 0.75 for 2020 which were 36.6, 45.2, 52.35, and 57.475.  The min, max, mean and median were 36.6, 65.3, 51.3, and 52.3.     

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
