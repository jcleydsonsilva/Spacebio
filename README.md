# SpaceBio Django Project

The SpaceBio's mission is to advance understanding of all researches outside Earth by providing exceptional access the space literature as a way smart through Artificial Intelligence and Machine Intelligence.

`This section of the README provides instructions on how to install dependencies and configure the database for the project.`
<br><br>

## Prerequisites

Before you begin, make sure to have Python and pip installed on your system.<br><br>

## Cloning the Repository

Clone this repository to your local environment:

```bash
git clone https://github.com/jcleydsonsilva/Spacebio.git
```
<br><br>

## Setting up the Environment for the SpaceBio Project

## Virtual Environment

After cloning the repository, set up a virtual environment using the following commands:

```bash
# Creating the virtual environment
python -m venv .venv

# Activating the virtual environment (Windows)
.\.venv\Scripts\activate

# Activating the virtual environment (Unix/Linux/MacOS)
source .venv/bin/activate
```
<br><br>
## Installing Dependencies

To install project dependencies, follow the steps below:

1. **Navigate to the Project Directory:**

```bash
# Navigate to the project directory
cd spacebio
```

2. **Install Dependencies:**

```bash
# Installing dependencies
pip install -r requirements.txt
```
<br><br>
## Configuring the Database
Edit the `spacebio/settings.py` file to configure the database information as needed.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spacebio',
        'USER': 'postgres',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
<br><br>
## Running the Development Server

Start the development server:


```bash
python manage.py runserver
```
