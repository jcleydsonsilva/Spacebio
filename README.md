# 🚀 SpaceBio

**SpaceBio Hub** is a platform designed to revolutionize access to space biology research. Our mission is to accelerate the understanding of extraterrestrial science by organizing, indexing, and analyzing space-related literature using the latest advances in Artificial Intelligence and Machine Learning.

Whether you're a researcher, data scientist, or simply passionate about space, SpaceBio Hub helps you explore and interact with scientific discoveries beyond Earth like never before.

---

## 🔧 Getting Started

This section provides a step-by-step guide to installing dependencies, configuring the database, and running the project locally.

### ✅ Prerequisites

Ensure you have the following installed:

- Python 3.8+
- pip (Python package installer)
- Git
- PostgreSQL 12+

---

## 📥 Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/jcleydsonsilva/Spacebio.git
cd Spacebio
```

---

## 🛠️ Environment Setup

### 1. Create and Activate a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.\.venv\Scripts activate
```

**Unix/Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. Install Dependencies

Run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

Before running the application, configure your PostgreSQL database.

Open `spacebio/settings.py` and update the `DATABASES` section as needed:

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

> Make sure PostgreSQL is installed and the specified database exists.

---

## 🚀 Run the Development Server

After completing the setup, start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to view the application.

---

## 📫 Contributing

We welcome contributions from the community! Feel free to fork the repository, open issues, or submit pull requests to help make SpaceBio even better.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
