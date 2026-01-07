---

# 📅 Event Scheduler – Flask Web Application

## 📖 Project Description

The **Event Scheduler** is a Flask-based web application designed to efficiently manage events and resources.
It allows users and administrators to create, view, update, and delete events, assign resources to events, and manage schedules using a centralized database.

The application is built with **Flask**, uses **SQLAlchemy ORM**, and **SQLite** for data persistence.
It follows a modular architecture with separate routes, models, and configuration files to ensure **maintainability** and **scalability**.

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, Jinja2 Templates
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Environment:** Python Virtual Environment

---

## 🚀 Features Implemented

* Create, edit, and delete events
* Resource management
* Assign resources to events
* SQLite database integration
* Flash messages for user feedback
* Modular Flask route structure

---

## 📂 Project Structure

```
New folder/
│── app.py
│── config.py
│── models.py
│── clear_db.py
│── remove_users.py
│── requirements.txt
│── events.db
│── instance/
│   └── events.db
│── routes/
│   ├── events.py
│   └── resources.py
│── templates/
│── static/
│── README.md
```

---

If you want, I can also:

* ✨ Make it **resume-ready**
* 🧪 Add **setup & run instructions**
* 📌 Add **API endpoints documentation**
* 📷 Add **screenshots section**

Just tell me 👍


---

## ⚙️ Installation Instructions

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd New\ folder
````

---

### 2️⃣ Create and Activate Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Database Setup

This project uses **SQLite**, so no external database server is required.

To initialize or reset the database:

```bash
python clear_db.py
```

Database file used:

```
events.db
```

---

## ▶️ How to Run the Application

```bash
python app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000/
```

---

## 🗄️ Database Schema Diagram

```
                       +------------------+        +--------------+
                       |      Event       |        |   Resource   |
                       +------------------+        +--------------+
                    +->| id (PK)          |        | id (PK)      |
                    |  | title            |        | name         |
                    |  | date             |        | type         |
                    |  | created_by (FK)  |        | availability |
                    |  +------------------+        +--------------+
                    |
                    |  +----------------------------------------+
                    +--| EventResourceAllocation                |
                       +----------------------------------------+
                       | id (PK)                                |
                       | event_id (FK)                          |
                       | resource_id (FK)                       |
                       +----------------------------------------+
```

---

## 🖼️ Screenshots of Major Screens

### 🏠 Dashboard

![Dashboard](screenshots/dashboard.png)

### 📆 Create Event

![Create Event](screenshots/create_event.png)

### 🧰 Resource Management

![Resource Management](screenshots/resources.png)

### 📋 Event List

![Event List](screenshots/event_list.png)

---

## 🎥 Screen-Recorded Demo Video 

👉 **Demo Video Link:**
[[Demo video link will be updated here](https://drive.google.com/file/d/1ltUlwVerHNbs8GtZ_XVOp-6ghlXtF7XU/view?usp=sharing)]

The demo video demonstrates:

* Application startup
* Event creation and management
* Resource allocation
* Database interaction

---

## 🧹 Utility Scripts

* `clear_db.py` – Clears all database tables
* `remove_users.py` – Removes existing users from the database

---

## 📌 Future Enhancements

* Role-based access control
* REST API support
* Email notifications
* Calendar integration
* Cloud deployment

---

## 👨‍💻 Author

**Name:** Wasim Ahamed
**Project Type:** Academic / Learning Project
**Framework:** Flask

---

## 📜 License

This project is developed for educational purposes only.

```
<img width="1920" height="1008" alt="dashboard" src="https://github.com/user-attachments/assets/992e491a-df46-4775-b03a-f01516a9e6a8" />
<img width="1920" height="1008" alt="create_event" src="https://github.com/user-attachments/assets/d3ee7e00-0f0d-41c0-ab15-b3e7c016e7e2" />
<img width="1920" height="1008" alt="resources" src="https://github.com/user-attachments/assets/f52ce8be-d351-4e3b-a4c6-97c0fbe2fc8c" />
<img width="1920" height="1008" alt="event_list" src="https://github.com/user-attachments/assets/0c0b0562-862c-4c34-9b68-88b8d3369df2" />
