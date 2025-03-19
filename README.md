# ToDo
#### Video Demo:  <https://youtu.be/aYCOO1lqW8I>
#### Description:
Simple web application using flask, html, css to create todo list.
It has register and login functionality allowing multible users, having their own to do list.

---

### Files:
###### Layout:
The layout used for the site is **layout.html** and it contains a navbar which has two states:
1. Register and Login links if the **session user_id** is **None**.
2. Hello, { username } if the **session user_id** isn't **None**.

It also contains a header for error massages.
After that there is the main block which will be replaced using jinja, by other *.html* files.
Finally a footer containing -Final Project For CS50 BY Ahmed Muhammad Ragab-.

---

###### Login:
The login page is implemented in **login.html** and its the main redirect for the user if he is not logged in,
it contains two text inputs and a submit button.
If the user input a wron name or password a massage will be **flased** indicating an error, without allowing the user to log in.

---

###### Register:
The register page is implemented in **register.html** and it allows new users to register in the site.
It contains three text inputs and a submite button.
If the user input no name or password, input an already registered name, or the repeated password does not match the password,
a massage will be **flased** indicating an error, without allowing the user to register.

---

###### todo·db:
This is the *SQL* database for the site, which has two tables, one for registered users, and one for saved users' todo lists.
The table schema is shown in the **schemma.db** file

`schema`

    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    );
    CREATE UNIQUE INDEX username ON users (username);

    CREATE TABLE todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id INTIGER,
        todo TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
---

###### helpers·py:
This file contains only one function responsable for decorating routes to require login,
which redirects the user to the login page if he/she is not loged in.

---

###### app·py:
This file is the main code for the wep app, it contains functions for handling varios requests of the sites pages and the database,
*Login
*Register
*Index

The filesystem is used not cookies in this app and cache is prevented
`code`

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

---

###### *static* foler:
Contains some styling for elemnts in the site like the red green logo, or the login/register form in the **style.css** file,
and the icon for the site.

`css`

    .red {
        color: red;
    }

    .green {
        color: green;
    }

    .form {
        margin: auto;
        background-color: #E8E8E8;
        width: auto;
        padding: 10px;
    }

    footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
    }
