# sqlalchemy-challenge
Module 10 Challenge for Morgan Bee

In this challenge, I used all of the class activites, Khaled's .ipynb notebook with class notes from GitLab, and class lectures to assist me in writing this code. I also asked our TA Andrew how the results of the last two app.routes were supposed to be displayed in the app_mb.py file. 

I also used the Xpert Learning Assistant to help me when I got stuck. Specifically, the Xpert Learning Assistant helped me manipulate the most_recent_date into datetime data type so I could calculate year_ago and use the variable in multiple queries. It also helped me understand that I needed to convert the whole DataFrame into datetime again before sorting in order to ensure the sorting was done properly. Xpert taught me how to make the bars in the bar chart thicker in order to match the expected output for that notebook cell. Finally, Xpert Learning Assistant helped me understand, in junction with the class notes and activities, how to implement use input to app routes and how to format the inputs in order to make your code work.
   
ChatGPT helped me with the problem in the notebook about finding the number of unique stations in the dataset. I was able to learnfunc.count(func.distinct()) in order to achieve that query. ChatGPT also helped me fingure out that I needed to use list(calculations[0]) in order to get the dictionary information to be jsonified for the last two app routes in the app_mb.py file. 

In the app_mb.py, I added some links for the static routes in order to make the website more accessible and easy to use. For the dynamic routes, I left them without links so that you are able to input the start and end dates as needed. I also added the session = Session(engine) and the session.close() for each app route. Although this may violate DRY, this was taught to us in class as good practice for developers to close your session once your query is complete. 

Overall this challenge required a lot of time and trial and error, and was an excellent learning tool for the skills in this module. 