# Gillian's Hmwk #7
## **Hello Jacob!**  &#x1F44B;
I hope you found my code wildly impressive (just kidding, I am still a newbie at this, but pretty proud of what I'm pulling off so far!)

I downloaded data for the "streamflow_wk7.txt" file on Friday 10/9/20.  If you want to up date to add one additional day, feel free, but I think it will be fine with the data as it stands so save yourself the extra work!

### Instructions for submitting my forecast:

  - Run code block at top of file to import modules and define functions.  

  - For Task 1:

    - Run through each block of "Run Cell" sections in sequence.   No output need be noted for forecasting yet, though I do print the dataframes to see the table format.
    - Only worry I have for this code is that the filepath won't work for your computer.  I hope all goes smoothly - I think it should since I housed the data folder right in snug with the .py file.  


  - For Task 2 and Task 3:

    - Run through each block of "Run Cell" sections in sequence and marvel at my amazing AR model r-squared value!  And then chuckle when you see how little data I am using to get that value trained! &#x1F606;


  - For Task 4: Note the key info to pull out and enter into the tables below:

    - Run first code block (AR Model) and note the values output from the AR model for "AR-1WK" and "AR-2WK".  Input those values into Table 2 below.  
    - The next two blocks in "Jill's Code" section print the historical minimum flow for the week and the statistics tables for the last 7 days.  I use these as discussion points in my markdown -  they are not needed by you as input for this assignment (based on instructions that you only need to pull the 4 final values and review via the rubric).
    - The next cell block plots a simple visual look at two-week flow trend.
    - Next few blocks get into finding the mean for the week and the percent change for flow values.   
      - I already entered in the variables that needed manual entry based on output for the dataset I ran.  If you download new data, you will have to manually enter in the variables output from code block on line 226 (first_val1 and last_val1) to variables on lines 236 and 237 (val_1wk_1 and val_1wk_2).
    - The block with the 'if statement' will return the value for my 1 week forecast  [JILL-1WK].
    - This code then repeats itself using the two-week data.
        - Again, I already entered in the variables that needed manual entry based on output for the dataset I ran.  If you download new data, you will have to manually enter in the variables output from code block on line 263 (first_va12 and last_val2) to variables on lines 273 and 274 (val_2wk1 and val_2wk2).
    - The final 'if statement' code block will output the two-week flow forecast value  [JILL-2WK].  
    - Enter these values into table 1 below and that's it!

# Written Assessment

The first thing I noticed is your print statements were very informative I will have to steal that idea for the next time I am having someone else run my scripts. Next, your graphs are nice and easy to understand. The variables were well explained instead of using x for instance you would use last_week_flow or something that would describe what this variable is. My to suggestions are minor but would save you typing extra characters. (1) on line 235 and 264 you type in values manually where you could again state that first_val2 = data_two_wks.head(1) that way you can just run the script w/o making change every week if you wanted, just by updating the week#. (2) on lines 246 and 283 there is and (if(condition): elif (condition):) statement you can simply use (if (condition): else:). else will run if conditions you defined are not met, this change is very minor though but would save you from accidentally missing a value for instance if you put 0 into your code it would return an error (although 0.00 % change is likely impossible so I don't think it would ever matter in this case). Altogether your code was great and easy to understand thanks Jill. Also, great job following PEP 8 standards.

# Forecast and Numerical Assessment

Table 1: One- and two-week forecast submission values  

|   | One-week Forecast  | Two-week Forecast  |
|--:|---|---|
| Jill's Code  | 72.3  | 67.3  |

Table 2: Regression-based one- and two-week forecast values  

|   | One-week Forecast  | Two-week Forecast  |
|--:|---|---|
| AR Model  | 75.53  | 85.16  |

Table 3: Code Rubric Scoring Table   

| Criteria  | 3 points   | 2 points  | 1 point  |
|--:|---|---|---|
| Readability  |  3 |   |   |
| Style  | 3  |   |   |
| Code Awesome  | 3  |   |   |  

![](assets/ReadMe-ff0ecab3.png)

Code Rubric Criteria here:
https://github.com/HAS-Tools-Fall2020/Course_Materials/blob/master/Assignments/Starter_Codes/code_review_rubric.md
