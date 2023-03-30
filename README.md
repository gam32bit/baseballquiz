<h1> baseballquiz </h1>

This is a simple web application that quizes users on players listed on projected opening day lineups for the 2023 MLB season. 

- I ran into some problems scraping player names initially because the websites I looked at first had complicated html, but I eventually found one that worked.
- Got picture scraper to work and insert directly into heroku database. When I tried to view table in terminal it showed up as a bunch of blank rows, I think because I'm converting the image data into binary. Not sure if there is a way around that, but it's working so it doesn't really matter.
- Ran into bug with the database URI - finally realized the uri needs to start with postgresQL - not postgres, for whatever reason.
- Also realized that storing the images in the database is too energy consuming to work on the web app. Instead I need to store the images in a folder, which I uploaded, but then convert the file names to safe file names and then store those names in the postgres table.
- The web app is now showing the images for the players. The counter is reseting after each guess, so I need to fix that. I also think that the scraper missed some of the players on the website, so I need to go back and fix that. 
- Made a better scraper, but some players do not have photos (not many) should double check that, also may want to drop the table and create a new one to make sure I'm working off of one source. I can't get the html and css to work, need to work more on that. Also now the counter points remain between sessions.
- Decided to just use json dict instead of database since I'm not working with that much data. 
- After I deployed there was an error with the session instance not maintaining after I clicked the submit button. Figured out it was because I needed to store secret key as an env var on Heroku.
- Last problem was restart button not working, session was not clearing. Solution was to create a separate restart function and have the button go there instead of trying to incorporate into index function.
