# Car Marketplace Project

## Introduction

This project is a Car Marketplace application built using Python and Tkinter for the GUI, and it interacts with a MySQL database to store and retrieve information about cars, sellers, users, and sales. The application provides various features such as user registration, adding new sales, fetching ratings, and querying car advertisements based on different filters.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Features

1. **User Registration:**
   - Users can register by providing their email, username, gender, date of birth, and phone number.

2. **Adding New Sales:**
   - Users can add new sales by specifying their email, seller name, car ID, and rating.

3. **Fetching Ratings:**
   - Retrieve the rating for a specific car sale, average rating by seller, and average rating by user.

4. **Querying Car Advertisements:**
   - Fetch car advertisements based on various filters, including brand, body type, year, and location.

5. **Statistics and Insights:**
   - Get insights such as the top 5 areas in Cairo for a specific brand and model, top 5 sellers, and top 5 brands/models by the number of listings.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/car-marketplace.git

## Database Setup
1. MySQL Database:
   Create a MySQL database named carstuff.
   Import the database schema using the provided SQL scripts (create_tables.sql).
2. Database Connection:
   Update the database connection details in the code (car_marketplace.py) with your MySQL host, username, password, and database name.

## Usage
1. Run the Application:
    python car_marketplace.py
2. Use the GUI:
    The application window will open, allowing you to register users, add sales, fetch ratings, and perform various queries.

## Dependencies
1. tkinter: GUI library for the Python standard library.
2. mysql-connector: MySQL database connector for Python.
