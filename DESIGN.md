# DESIGN

There are three “layers” to our project: the client-side website, the SQL database, and the Python code that helps them communicate
with each other. We’ll go through the front-end and back-end separately and explain our design choices.

# WEBSITE: HTML, CSS, JavaScript

We wanted the website to be easily navigable and self-explanatory to use, as well as look clean. That’s why we went with a search
bar as the homepage; everyone knows how to use Google, and so everyone should recognize what the purpose of the website is for
when they arrive at the homepage. Furthermore, a 40,000+ entry database is overwhelming to browse through to find what you're
looking for, so an autofocused search lets you immediately find anything, whether broad ("symphony") or specific ("Trio for horn,
violin, and piano in E-flat, Op. 42"). If you want to refine your search by category, you can do so, but we figured that an
unspecified search option is the best default. Of course, you might want to view the entire database, so that's an option in the
navigation bar.

The search and the view database both lead to the same interface: a table of the relevant records. We decided to show 100 records
per page: enough to provide ample results without having to load a new page, but not so much that it slows down the website. Next
and previous buttons at the top and bottom let you scroll through the pages. Though there are a few more fields than are shown, such
as id, flagged, and comment, we chose to show only the most relevant information.Those other three fields are shown by clicking on
the row -- it is an accordion table, so another row pops out below. We needed to show the id to be used in our implementation of
flagging, which is a button right in the row as well as a navigation button. Comment and flagged are only shown if they exist.

Adding records and adding comments are both forms that require all fields to be entered (except notes) to be submitted. We capitalized
on our experience from Finance to implement this. In addition, we made it so that only logged-in users (admins) could add a record,
so as to avoid any unwanted additions.

Finally, we used the Bootstrap `alert` and `modal` classes to implement the alerts and the pop-up, as well as a Bootstrap template
for the site itself.

Aesthetically, we wanted to give some WHRB flavor to the site, so we made sure the station logo was in the header and that the
favicon was our mascot, the penguin!

# DATABASE: PYTHON & SQL

What we thought would be the easiest part of the project actually turned out to be most difficult (it took all of the hackathon to
figure it out! at least we got pancakes in the end...?). We thought that importing the .csv file from the original Master Chekhov
into chekhov.db would be easy, but there were several roadblocks along the way. First of all, due to the commas in many of the titles,
we could not use commas as delimiters. We ended up having to go into the Windows settings of Chris's laptop to change the
delimiters from commas to asterisks (because semicolons didn't work either!). Then we tried importing, but it only worked if we
imported smaller chunks of 200 rows at a time instead, and no accents or special characters showed up. We had to explicitly
define the character encoding as UTF-8, which allowed characters from foreign languages to show up. But STILL we couldn't import
straight into chekhov.db using the phpLiteAdmin interface, so we ended up creating a python file called `loader.py`, which went
row by row and imported the .csv file.

After that, everything was fairly straightforward. We use `db.execute` in the search functionality, adding a record, making
a comment, registering, and logging in (anything that had to do with editing the database). SQLite didn't support the concatenation
functionality we wanted in order to add a new comment to the notes field without replacing what was previously in there (we got some
weird results, like previous comments being written in twice), so we made a list in python, pulled data from the table, appended
the new comments to the list, and then updated the table.

Search was especially SQL-heavy. Essentially, the way it works is that we created a list in Python of the clauses of our SQL query,
then joined them into a string, which we then executed using `db.execute`. We realized halfway through that in order to accommodate
multiple keywords in our search like real search bars and engines we had to implement more dynamic SQL queries into our Python. The
way we tackled this problem was to create a program in Python that would take the searchtypes and queries and generate SQL queries.
We used logic statements to create relationships between the search terms depending on whether is was everything or a specific clause.
We also chose to use the redirect functionality of Flask rather than simply rendering the index template right after submitting the
search form in order to retain the search queries in the url, allowing us then the option of including pagniation features. In order
to implement the next and previous buttons on our index page, we chose to use the OFFSET and LIMIT functionality of SQL, passing in
varying OFFSET values using javascript. We also attempted to implement first and last page buttons, but unfortunately we weren't able
to find a good solution because we wanted to focus above all on maintaining a smooth and fast user experience, but counting the number
of rows each time we searched to create a last page button would force the website to load all the rows at once.