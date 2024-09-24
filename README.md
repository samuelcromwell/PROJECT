# Vantage Drive Management System

This is a web based management system for Vantage Driving School, this system enables the trainees and instructors to interact, whereby the trainees can book lessons based on the instructors schedules, and also view their progress whereas the instructors set the schedule and update individual learner progress. The admin manages and oversees all the activities happening in the system and approves new trainees who have been signed up. There is also a mechanisms for the trainees to be able to pay their fees using Mpesa

# Project Setup Guide

## Introduction

This guide outlines the steps required to set up the project on your local machine. Follow the instructions below to clone the repository, set up a virtual environment, install dependencies, and run the project.

## Prerequisites

Make sure you have the following installed:
- Python 3.11.9
- Git

## Installation Instructions

### Step 1: Clone the Repository

Start by cloning the project repository to your local machine, using

git clone https://github.com/samuelcromwell/PROJECT.git
then 
cd into the local folder

### Step 2: Create a Virtual Environment
Do this by running;

'python3 -m venv venv' 

where the second venv represents the name of you rvirtual environment

### Step 3: Activate the Virtual Environment
For macOS/Linux:
source venv/bin/activate

For Windows:
venv\Scripts\activate

### Step 4: Install the Dependencies
'pip install -r requirements.txt'

This will install all the required dependencies as listed in the requirements.txt file.

### Step 5: Run the Development Server
python manage.py runserver

The server will start, and you can access the application at http://127.0.0.1:8000/.

## Admin Credentials
To access the admin panel and perform admin actions, use the following credentials:

Username: vantageadmin
Password: admin123

## Trainee Credentials
To login as a trainee, use the following credentials:

Username: Trainee1
Password: vantage@2024

## Insructor Credentials
To login as an instructor, use the following credentials:

Username: Instructor1
Password: vantage@2024

## Additional Information
To quit the development server, press CTRL + C.
Make sure to run the project inside the activated virtual environment.

## Troubleshooting
If you encounter any issues, ensure all dependencies are installed correctly and that you're using the correct Python version.

## Author
Developed by Samuel Cromwell