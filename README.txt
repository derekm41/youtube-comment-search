In response to a popular youtube channel where the host has the viewers guess completion time of a project. The viewer who guesses the closest to the actual completion time wins.
The comment section of youtube can be hard to manually de-cypher who guessed correctly. 

* Using the google api for youtube I extracted all comments from a given video focusing on specific data provided by the api.
* I needed to parse the comment to extract the relevant guess. Assuming that most completion time guesses will be in this format: I guess 12 hour 35 min 54 sec! (or similar version). 
    I parsed the comment to extract Hour, Minute, and Second data.
* Once the comment is parsed I extract the data to a csv so I can filter the data based on the actual completion time. 

60,000+ video comments can now be checked and winner found in a matter of minutes. 


***
Problems with this approach surround the formatting of the actual guess. It's difficult to account for edge case formatting that doesn't follow our assumed formatting. 

_______________________________________________________________________________________
Goals for improving project.

* Rebuild the extraction function. Possibly utilize librarys like nltk or spaCy to analyze the text comments.

* Upgrade the output. Rather than export a csv provide the top three closest guesses in the output. 

* Push to cloud for use off main machine.

* Build a simple web front end so tool can be used online.

*** Need to complete project so that it can be more end to end project ***
