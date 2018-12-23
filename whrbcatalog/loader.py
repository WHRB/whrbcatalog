# pylint: disable=C0103
"""
Data loader
"""
import csv
from cs50 import SQL
# from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chekhov.db")


# Used to load the CSV into SQLite because the import function in phplite was broken
def main():
    """Import data"""
    with open('chekhov.csv', 'r', encoding='UTF-8', newline='') as f:
        reader = csv.reader(f, delimiter="*")
        for row in reader:
            a = row[0]
            b = row[1]
            c = row[2]
            d = row[3]
            e = row[4]
            f = row[5]
            g = row[6]
            h = row[7]
            i = row[8]
            j = row[9]
            k = row[10]
            notes = row[11]
            m = row[12]
            db.execute(("INSERT INTO library VALUES (:ID, :period, :composer, :title, :artist, :label, :format, "
                        ":number, :length, :times_played, :last_played, :notes, :flagged)"),
                       ID=a, period=b, composer=c, title=d, artist=e, label=f, format=g,
                       number=h, length=i, times_played=j, last_played=k, notes=notes, flagged=m)


if __name__ == "__main__":
    main()
