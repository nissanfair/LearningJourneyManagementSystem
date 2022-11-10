# Project Title
Learning Journey Management System

# Description
A system to improve the company All-For-One's learning culture among employees.
Does CRUD for Jobroles, Skills and learning journey. 
Application backend: Python Flask
Application Frontend: html, bootstrap, javascript

# Importing CSV File:
<ol>
  <li>Type localhost in url</li>
  <li>Access PHPMyAdmin and login</li>
  <li>Go to the ljms schema</li>
  <li>Under Course, Role, Staff and Registration import the respective CSV</li>
  <li>Ensure the following checkboxes are ticked when importing: </li>
  <li>Update data when duplicate keys found on import (add ON DUPLICATE KEY UPDATE) & Do not abort on INSERT error</li>
</ol>

# How to start the application:
<ol>
  <li>Check api_app.py file, change the configurations(DBpassword, DBport, DBusername, DBhost, DBname) accordingly</li>
  <li>Those are for connecting to the database</li>
  <li>Run WAMP/MAMP</li>
  <li>Run the api_app.py file</li>
  <li>Open Home/index.html to access the homepage</li>
  <li>You can start using now!</li>
</ol>

# Understanding application folder:
<ol>
  <li>.github/Workflow Folder: Contains CI yml file to run CI pipeline on push</li>
  <li>api_app.py: All the Backend code</li>
  <li>Courses, Home, LJourney, Role, Skills Folders: Frontend html and js codes</li>
  <li>RawData Folder: Contains CSV data given by product owner</li>
  <li>integration_test.py & unit_test.py: Unit & integration testing codes</li>
</ol>

# GitHub Link
https://github.com/Zuhayley/ljms_spm.git
