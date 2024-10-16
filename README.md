Food Delivery App

This app  allows you to ordering food as customers on the other hand the restaurants can manage the orders by using restoran that have been 
ordered by customers by using kullanıcı_app.py.

Getting Started

Prerequisites

  To run this project, ensure that you have the following installed on your system:

  Python 3.x
  Required Python libraries:
    Flask
    SQLAlchemy
    Flask-Login
    Flask-WTF
    Jinja

Clone the repository: git clone [repository URL]
Navigate to the project directory: cd food_delivery_app
Set up the database: python models.py
Run the application: python restoran_app.py (for restaurant management) python kullanıcı_app.py (for customers)

After running the application, you can access it through the local server at http://127.0.0.1:5000/.

Project Structure

  code_maker.py: Contains helper functions for the project.
  kullanıcı-app.py: Handles user-related operations such as registration and login and ordering products.
  models.py: Defines the database models for users, restaurants, and orders.
  restoran_app.py: Main application file that runs the Flask server and handles restaurant-related features.
