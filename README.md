# notes_application
A Flask-based notes-taking web app with user registration, login, and MySQL database integration. Users can add, view, and delete notes with a clean, responsive UI.

This is a simple notes-taking web application built using Flask (Python) for the backend and HTML/CSS/JavaScript for the frontend. The application stores notes in a MySQL database using SQLAlchemy ORM. It includes features like user registration, login, adding/deleting notes, and displaying sample notes in a responsive layout.

Features:

User Authentication:
  
  1.Register with name, email, password
  
  2.Password validation tooltip: requires at least 1 uppercase, 1 special character, 1 number, and minimum 5 characters
  
  3.Login page with redirect to dashboard on success

Notes Management:

  1.Create new notes
  
  2.View all notes for a user
  
  3.Delete notes
  
  4.Sample notes shown in a card carousel layout
  
Frontend UI

  1.Responsive cards using CSS
  
  2.Carousel display for sample notes
  
  3.Tooltips and styled input popups for better UX
  
  4.Connected static folder for CSS and images
  
Tech Stack:

  Backend - Python + Flask
  
  Frontend - HTML, CSS, JavaScript
  
  Database - MySQL
  
  ORM - SQLAlchemy
  
DataBase Queries:

  To Create database:
  
    create database notesapplication;
    
  To Create User Table:
  
    create table notesapplication.user(
      user_id VARCHAR(36) NOT NULL PRIMARY KEY,
      user_name VARCHAR(255) NOT NULL,
      user_email VARCHAR(45) NOT NULL UNIQUE,
      password VARCHAR(45) NOT NULL,
      last_update DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      create_on DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

  To Create Notes Table:
  
    create table notesapplication.notes (
      note_id VARCHAR(36) NOT NULL PRIMARY KEY,
      note_title VARCHAR(200) NOT NULL,
      note_content VARCHAR(255),
      last_update DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      create_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      user_id VARCHAR(36) NOT NULL,
      FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
    );
    
  To Create Sample_notes table:
  
     create table notesapplication.sample_notes(
      id INT NOT NULL AUTO_INCREMENT,
      title VARCHAR(200) NOT NULL,
      content VARCHAR(255) NOT NULL,
      PRIMARY KEY (id)
    );
  
  
