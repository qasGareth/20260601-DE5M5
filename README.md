# 20260601-DE5M5

## Scenario:
  A library wants to improve their current quality analysis, looking for a more efficient way to clean data    using python.
  Input is 2 flat files, one records checkouts/returns, the other is a list of customer IDs and names
  In the checkout/4returns file, Book Checkout is stored as a string, Days allowed to borrow is also a string that isn't in days, some books are borrowed for a negative amount of time
  In the customer file, some customer IDs and customer names are missing
  There is no Customer ID 4 in the customer file, but that customer did borrow a book
  

## User Stories:
# Book Checkout:
As a data analyst, I want the Book Checkout field converted from a string into a proper date type, so that I can reliably sort, filter, and calculate durations on checkout activity.

# Days allowed to borrow:
As a data analyst, I want the "days allowed to borrow" field standardised into an integer number of days, so that loan periods are comparable across all records regardless of how they were originally entered (e.g. "2 weeks", "1 month").

# Impossible loan durations
As a data analyst, I want records where a book was returned before it was checked out (negative borrow time) identified and quarantined, so that they don't distort reporting on average loan length.

# Missing customer IDs
As a librarian, I want records with missing customer IDs flagged, and I want customer records with a valid ID but missing name flagged for follow-up, so that incomplete profiles are tracked and amended

# Cross-file integrity
As a data analyst, I want every customer ID appearing in the checkout file validated against the customer file, so that checkouts tied to a customer who doesn't exist in the customer list (like ID 4) are caught as referential-integrity errors.

# Overall End-User Story
As a librarian, I want the cleaning process to run automatically on the two input files and produce a cleaned output plus an error report, so that I can refresh the data quality analysis without manual editing each time.

## Solution Diagram:
<img width="2208" height="1164" alt="image" src="https://github.com/user-attachments/assets/696036ba-983f-459e-9b33-08dfe483a566" />

## Power BI Dash:
<img width="1358" height="762" alt="image" src="https://github.com/user-attachments/assets/9090c83a-e783-4c79-80db-d8a685cac59d" />
