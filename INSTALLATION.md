# Weather Laundry - Installation guide
This guide will help you set up and run the Weather Laundry project locally.

## Prerequisites
Make sure you have the following installed:

- Python 3.11+
- pip

## Installation Step by Step

### 1. Clone the Repository 
``` bash
git clone https://github.com/SariyaP/weather_laundry.git
```
### 2. Create and activate Virtual Environement
```bash
python -m venv .venv
```
#### Windows
```bash
.venv\Scripts\activate
```
#### macOS/Linux
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
#### Well-Known trouble while installing Requirements
We have discovered that there might be problem with pandas and other packages so try running the app and install the missing package manually again.

#### Troubleshooting with pandas long installation
Kill the current process by pressing Ctrl-C and install pandas manually again
```bash
pip install pandas
```

### 4. Run the app
Go to the baackend directory
```bash
cd backend
```
Run the app.py
```bash
python app.py
```
Note: You can run app.py after you have created config.py. The template is in config.py.example

The API will be avaliable at:
```bash
http://127.0.0.1:8080/laundry-api/v1
```

API docs:
```bash
http://127.0.0.1:8080/laundry-api/v1/ui/
```

### 5. Run the frontend
Go back to the root directory
```bash
cd ..
```
Go to the frontend directory
```bash
cd frontend
```
Run Django
```bash
python manage.py runserver
```
