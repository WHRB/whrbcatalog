Welcome to the Master Chekhov! This website is a searchable online database of all 40,000+ tracks in WHRB’s physical library down
in Pennypacker basement. Here’s how you can use the site.

First, you should be able to access the site by executing the `flask run` command in the terminal.

Upon entering the site, you will be brought to the homepage, which is a simple search page. Let’s say you want to see all the tracks
in WHRB’s library that were composed by Bach. Then, in the “Search by” dropdown menu, select “Composer” and type `Bach` in the search
bar. Be sure to actually search something, or you’ll get an alert. Click “Submit,” and every track that has something similar to
“Bach” listed as the composer will come up as a result! You can similarly search by period (WHRB Classical DJs sort the music into
7 time periods, 0 through 6, for ease of classification), title, artist, label, and length. We envision this search function being
particularly useful if you’re searching by length or period, because DJs are often looking for a piece to fill a particular duration
of time or a piece from a particular era, without having a specific title in mind.

If you look in the navigation bar, you’ll also see a “View Database” page. This is simply a paginated table of the tracks in the
database. (Click on “Next” and “Previous” to go through the database.) If you hover over the rows of the table, you’ll also notice
that you can expand each row to show some extra information. This information includes the track’s unique ID in the database,
whether or not it has been flagged, and some comments, which could include why it was flagged (damaged? missing?), what listeners
think of the piece, or some interesting history behind the piece. (This expanding to reveal extra information feature is also
available in the search results.)

When you expand a row, you’ll also see a button called “Flag.” If you click on this button, a form will pop-up, asking you for the
track’s unique ID and the reason for your comment. Go ahead and submit, and when you go back to view that track’s information, your
input should be there!

Another way to flag a record (or otherwise add a comment associated with the record) is to go to the “Make Comment” page. You’ll
see the same form, with the same functionality. Again, if you do not enter all the information, you will be alerted.

The last page in the navigation bar is the “Add Record” page. The purpose of this page is to input any loose tracks that are not
currently in the WHRB Chekhov. Simply fill out the information (make sure none is missing, or else you will get an alert!), and
your track will be added.

Note that the “Add Record” pages are only available to users with the login. To register, simply click the
“Register” button in the top right and you will be brought to a registration page, where you will be asked for a username and
password. Similarly, there is a button to log in right next to the “Register” button. If you try to register with an existing
username, you will get an alert and the page will refresh so that you can reregister.