# Team MJJ Forecast
*Mekha, Jill, Jake*

*11/09/2020*

---------
#### Forecast Values

**XXX** cfs for 1 week forecast and **XXX** cfs for 2 week forecast

---------
#### Summary of Collaboration

<ins>How We Put the Pieces Together</ins>

Jake is near the top of the leader board for the 1 and 2 week forecast, so we decided to use his script as the basis for our 1 and 2 week forecast. Based on the RMSE plots from last week, Jill's error was pretty low for the 16 week forecast so far, so we decided to use her script as the basis for our long term forecast. We decided to use Mekha's script as the basis for our map, because its extent and choice of layers made the Verde Watershed easiest to visualize.

<ins>Who Did What</ins>
* Step 1: Mekha took first pass at combining Jake's two week forecast script with Jill's 16 week forecast script, getting everything running, and doing some code cleanup and organization. Mekha also incorporated temperature data into Jake's regression model.
* Step 2: Jake incorporated temperature into the 1 and 2 week forecast loop based on the new regression model, and moved functions into a separate script.
* Step 3: Jill added code from previous weeks to 16 week forecast, cleaned up the map, and added time series graphs of the model input data (streamflow, precipitation, and temperature)
* Step 4: Mekha took first pass at markdown file, and Jake and Jill

---------
#### Summary of forecast approach

A 1 week, 2 week, and 16 week long-term forecast was made for the Verde River streamgage near Camp Verde, shown on the map below.

*INSERT MAP HERE*

<ins>1 and 2 Week Forecast Approach</ins>

For the 1 and 2 week summary, we used a linear regression model with the following input variables: average weekly flow from 1 week prior, average weekly flow from 2 weeks prior, average weekly flow from 3 weeks prior, average weekly precipitation, and average weekly max temperature. Recent observed streamflow is an intuitive predictor of future streamflow. Precipitation has become a more important predictive variable with winter rains beginning. And average maximum temperature is a valuable predictive variable for streamflow during Arizona's extended periods of no precipitation because temperature can act as a proxy for other processes that impact streamflow, such as snowmelt and leaf out in the spring. The input variables are shown in the timeseries graph below.

*INSERT TIMESERIES OF PREDICTIVE VARIABLES HERE*

<ins>Long-Term Forecast Approach</ins>

For the 16 week forecast, the approach used was to focus on observed historical minimum precipitation values. This approach recognizes that 2020 has been a low flow year. Instead of weekly average flow, a dataframe of weekly minimum flows was created. Then for each of the 16 weeks of interest, the minimum from the period 1989-2019 was chosen as the 16 forecast value for 2020.
