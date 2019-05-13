# HebrewDateReminder
Generate ICS file of Hebrew Dates converted to Secular Dates


(Work in progress)
This program is intended for users who have long lists of hebrew dates that they'd like to be reminded of.
A member of a large Jewish family, for instance, would have trouble keeping track of all the hebrew birthdays,
anniversaries and passings in their immediate and extended family. 

It is difficult to track these hebrew dates with modern calendars in order to get reminders for upcoming events
as the dates change every year. This is because the hebrew calendar follows a lunar cycle while the secular/gregorian
calendar follows a solar cycle.

As an example, Rabbi Menachem Schneerson's birthday took place on the hebrew date of Nisan 11th, 5662.
On that year, Nisan 11th fell out on April 18th, 1902.
However, in 2019 it will fall out on April 6th, in 2020 it will fall out on April 5th, and in 2021 it will fall out on March 24th.

https://www.hebcal.com/ provides free services to convert between hebrew and secular/gregorian dates - one date at a time.

This program uses hebcal's API to take a list of hebrew dates, convert them to their secular equivalents for the upcoming 5 years,
and then generates an ICS file with all those dates. The ICS file can then be imported into Google Calendar, Outlook or any other
Calendar program.
