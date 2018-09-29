# Pyghack2018
Code for Pyghack 2018 Project to tackle the CUMTD Bus Congestion Problem: 

# COMBATING BUS CONGESTION
## Organization Name: 
Champaign - Urbana Mass Transit District (CU-MTD).
 
## Local Sponsor: 
Ryan Blackman from CU-MTD.

## Overview:
MTD helps our communities thrive by offering individuals, organizations, and municipalities what they need to get to what matters. Whether it’s getting you across town to work or doing our part in to change mobility in our region, expand Champaign’s downtown, or strengthen the connections between the University of Illinois and surrounding communities for good, MTD is a reliable partner and we’re here when you need us. 

## Problem Statement: 
During the school year, bus traffic at stops around campuses fluctuates dramatically depending on the time of day. There are periods of ‘near-empty’ buses and periods of ‘sorry you cannot get on’ traffic. This project aims to identify the time and locations where bus demand is high. One possible direction is to investigate the relationship between bus traffic and location of academic buildings and class schedule at U of I, since bus demand from students tend to get much higher when they get out of classes. The insights may help CU-MTD to adjust bus schedule accordingly and improve the riding experience for passengers at on-campus stops.

## Evaluation criteria:
* Effective and compelling visualization of bus stops and bus stop traffic.
* Reasonable identification of hot spots (location and time).
* Viable suggestions for optimizing bus routes and bus schedules.
 
## Datasets:

|Data|Content|
|----|-------|
|General Transit Feed Specification (GTFS): https://developer.cumtd.com/|The GTFS, developed by GoogleTM , in conjunction with several other transit agencies, is an open format that defines schedule and geographic information for public transport systems. The original intention was to create a format to power Google MapsTM.The GTFS datasets contain information about bus routes, locations of stops, and trip schedule for CU-MTD public transportation system. The zip file contains the following files: *agency.txt, calendar.txt, calendar_dates.txt, routes.txt, shapes.txt, stop_times.txt, stops.txt, trips.txt.* Detailed definitions of fields in datasets from GTFS are available at https://developers.google.com/transit/gtfs/reference/?csw=1|
|Courses Data|<ul> <li>**Enrollment**: Number of students in all classes coded by class CRNs.</li> <li>**Schedule**: The meeting time and location for all classes coded by class CRNs are put together in a big csv file. Some preproceessing is needed. The pdf file frow which the csv was extracted is also provided.</li> </ul>|



