# Maintenance Request Ticketing System
## Project for ITCS 6112

### Description:
Our project seeks to provide a web application that is an all-in-one portal for tenants and property managers alike to improve the handling of maintenance requests. The system includes a centralized dashboard for property managers to monitor, prioritize, and process maintenance requests, while tenants are provided with an easy-to-use interface through which they can submit and follow their requests in real time.

This solution is designed to simplify communication, streamline operations, and ultimately enhance tenant satisfaction. By reducing administrative hassle and improving collaboration between teams, it offers a practical, scalable solution for property maintenance teams today.

The project has reached its core development milestone, and it is now a complete application that addresses both functional and non-functional requirements.

### Features:
- **User Authentication & Role Management**: Tenants and property managers can securely log in and are redirected to their respective dashboards with session management.
- **Ticket Creation & Management**: Tenants can submit maintenance requests with optional photo attachments, view their submitted tickets, and edit ticket details as needed.
- **Property Management Dashboard**: Property managers have access to a centralized dashboard to view, sort, and manage all submitted tickets in real-time. They also have a personalized dashboard to track and manage tickets specifically assigned to them.
- **Ticket Assignment & Status Updates**: Property managers can assign tickets to themselves, update progress (Submitted, In Progress, Complete), and add internal comments with optional photo attachments.
- **Photo & Comment Tracking**: Property managers can upload photos and comments to document the repair process and facilitate updates to tenants.
- **Email Notifications**: Automated email alerts notify property managers of new submissions and tenants of status updates, comments, or ticket closure.
- **Data Validation & Security**: Input sanitization and session-based access control were implemented to ensure data integrity and user privacy.
- **Analytics Overview (Property Manager)**: Property managers can view real-time metrics including the number of total, open, in-progress, and completed tickets to assess workload.

### Tech Stack
This project was built using the following technologies:
- Python – Core programming language used for backend development
- Django – Web framework used to handle routing, logic, authentication, and ORM
- SQLite – Lightweight, file-based database used via Django’s built-in configuration
- HTML & CSS – Used to structure and style the frontend
- Bootstrap – Framework used for responsive design and UI components

### Team Members:
- Dalton Corriher
- Jessy Gillespie
- Vanessa Kelly
- Monnish Sayi Reddy Peta
- Hayley Siharath
- Jadon Vanschaick

### Deployment Instructions
Download and install the latest version of Python. Latest version can be found at the link provided below.
https://www.python.org/downloads/ 
Git clone the latest version of the project from our repository linked below.
https://github.com/dmangames1941/Maintenance-Request-Ticketing-System 
Open a GitBash terminal
If GitBash is not installed, it can be found here: https://git-scm.com/downloads 
Navigate to the project folder. Your terminal should show something similar to the following file path:

In the terminal, run the following terminal commands (Note this is only for windows. Mac will follow different instructions):
$ python -m venv .venv 
The following folder will appear after the command is ran

$ cd maintReqTickSys
$ source .venv/Scripts/activate
$ pip install -r requirements.txt
$ py manage.py runserver
