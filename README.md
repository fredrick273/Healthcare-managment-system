# Healthcare Information System

The Healthcare Information System is a comprehensive web application developed using the Django framework in Python. It aims to streamline various processes within a healthcare facility, enhancing efficiency and patient care.

## Features

- Patient Registration and Management
- Employee Management (Doctors, Nurses, Administrative Staff)
- Appointment Scheduling
- Pharmacy Management (Inventory, Billing, Prescriptions)
- Prescription Management
- Laboratory Test Ordering and Result Tracking
- Report Generation (Prescriptions, Lab Results, Pharmacy Bills)
- User Authentication and Authorization

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python (version 3.6 or later)
- Django (latest stable version)
- PostgreSQL or MySQL (Database Management System)

### Installation

1. Clone the repository:
```
git clone https://github.com/fredrick273/Healthcare-managment-system.git
```
3. Create a virtual environment and activate it:
```
python -m venv env
source env/bin/activate  # On Windows, use env\Scripts\activate
```
4. Install the required Python packages:
```
pip install -r requirements.txt
```
5. Set up the database:

   - Create a new database for the project.
   - Update the database settings in `settings.py` file with your database credentials.

6. Apply database migrations:
```
python manage.py migrate
```
7. Create a superuser (admin) account:
```
python manage.py createsuperuser
```
8. Start the development server:
```
python manage.py runserver
```
The application should now be running at `http://localhost:8000/`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
