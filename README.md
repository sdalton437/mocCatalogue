# mocCatalogue

This code hosts an application on your local machine, which is a fictional catalogue for the McGill Outdoors Club.
When not logged in, the user is able to navigate the sports and items of the database. The user has the ability to 
log in with Google, and once logged in has the ability to create, edit or delete items. 

# Requirements

This code requires the [fullstack-nanodegree-vm-master virtual machine](https://github.com/udacity/fullstack-nanodegree-vm), 
and python 2.7. You will also need client_secrets.JSON, database_setup.py, views.py, lotsofitems.py, and all files in 
the static and img folders. 

First, bootup your virtual machine using `vagrant up` within the vagrant directory, and then login
using `vagrant ssh`. You must first run lotsofitems.py to populate the database, and then run views.py to
launch the application on your local machine. 

Open up a browser, and the application is launched on localhost:5000
