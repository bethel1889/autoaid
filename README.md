# AutoAid 🚗🛠️

**AutoAid** is a web application designed to connect skilled mechanics with customers in need of car repair services. Whether you're a car owner looking for trusted mechanics nearby or a mechanic seeking new clients, AutoAid bridges the gap with ease.

---

## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Setup and Installation](#setup-and-installation)
5. [Technologies Used](#technologies-used)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features

- 🔍 **Search for Mechanics**: Locate trusted mechanics by region or specialty.
- 🛠️ **Report Issues**: Describe car issues in detail for faster resolution.
- 📝 **Profiles for Mechanics and Customers**: Create, view, and edit profiles to showcase services or track reported issues.
- 📍 **Location-Based Filters**: Filter mechanics and issues by location for convenience.
- 📄 **Comprehensive Admin Tools**: Manage users and rooms effectively.
- 🎉 **User-Friendly Interface**: Clean, responsive design for all devices.

---

## Getting Started

Follow these instructions to set up AutoAid locally.

### Prerequisites

- Python 3.10 or later
- SQLite
- pip (Python package manager)

---

## Project Structure

```plaintext
autoaid/
├── app.py                  # Main application logic
├── database/
│   ├── auto_aid.db         # SQLite database file
│   ├── db_builder.py       # Script for database seeding
│   ├── schema.sql          # Database schema definition
├── flask_session/          # Session files
├── helpers.py              # Utility functions and decorators
├── requirements.txt        # Python dependencies
├── static/
│   ├── styles.css          # CSS for styling
│   ├── fix-icon.svg        # Application logo
│   ├── favicon.ico         # Favicon
├── templates/
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── profile.html        # User profile
│   └── ... (other templates)
└── README.md               # Project documentation
```

---

## Setup and Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bethel1889/autoaid.git
   cd autoaid
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**

   - Create the database:
     ```bash
     sqlite3 database/auto_aid.db < database/schema.sql
     ```
   - Optionally seed data:
     ```bash
     python database/db_builder.py
     ```

5. **Run the Application**

   ```bash
   flask run
   ```

6. **Access the Application**
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Technologies Used

- **Backend**: Flask, SQLite
- **Frontend**: Bootstrap, HTML5, CSS3
- **Others**: Gunicorn (for deployment), CS50 Python Library

---

## Usage

### Key Pages and Their Functions

- `/` - Home page with navigation.
- `/register` - User registration.
- `/login` - User login.
- `/profile` - View and manage personal profile.
- `/mechanics` - Find mechanics by location.
- `/issues` - View and report car issues.

---

## Contributing

We welcome contributions to improve AutoAid! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

Feel free to provide feedback or raise issues [here](https://github.com/bethel1889/autoaid/issues).
