# 🚀 Mars Mission CRUD App

## **Description**
The **Mars Mission CRUD App** is a student project. Built with **Flask**, **SQLite**, and **Docker**, it provides a RESTful API and a simple UI for CRUD operations. The project includes a **CI/CD pipeline** (GitHub Actions) for automated testing, Docker image builds, and secure deployment.

---

## **Key Features**
- **📦 CRUD Operations**: Manage resources via API or web UI
- **🧪 Automated Testing**: Unit tests with `pytest` (86% coverage) + code quality checks with `pylint`
- **⚙️ CI/CD Pipeline**:
  - Linting, testing, and Docker image builds on every commit
  - Automatic push to Docker Hub on `main` branch updates
- **🐳 Infrastructure as Code**:
  - Docker Compose setup (Flask + Nginx)
  - Persistent SQLite database with volume mounting
- **🖥️ Simple UI**: Vanilla JavaScript frontend

---

## **🚀 Quick Start with Docker Compose**
**Prerequisites**:
- Docker and Docker Compose installed
  - On **Windows/macOS**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop).
  - On **Linux**: Install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/).

1. **Clone the repository**:
   ```bash
   git clone https://github.com/xaris96/Mars-Mission.git
   cd Mars-Mission
   ```

2. **Start the stack**:
   ```bash
   docker-compose up --build
   ```
   > **Note**: This command rebuilds the Docker image every time to ensure the latest changes are included.

   To stop the stack, use:
   ```bash
   docker-compose down
   ```
   > **Note**: This command rebuilds the Docker image every time to ensure the latest changes are included.

3. **Access the application**:
   - Web UI: `http://localhost` (or `http://127.0.0.1:5000` if running Flask directly)
   - API Endpoints:
     - Get all users: `GET /api/users`
     - Add a user: `POST /add`
     - Edit a user: `POST /edit`
     - Delete a user: `POST /delete`

---

## **🛠️ Development Setup**
### **Run Locally (Without Docker)**
1. Clone the repository:
   ```bash
   git clone https://github.com/xaris96/Mars-Mission.git
   cd Mars-Mission
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -c "from app import init_db; init_db()"
   ```

5. Start the server:
   ```bash
   python app.py
   ```

6. Access the application at: `http://localhost:5000`

---

### **Run Tests**
To run the unit tests inside the Docker container:
```bash
docker-compose run app /venv/bin/pytest --cov=app
```

---

## **📂 Project Structure**
```
mars-mission/
├── app.py               # Flask backend
├── static/              # Frontend assets
│   └── app.js           # JavaScript logic
├── templates/           # HTML templates
│   └── index.html       # Main UI
├── data/                # Runtime database storage, created locally
├── test_app.py          # Tests for the Flask app
├── nginx.conf           # Nginx configuration file
├── Dockerfile           # Container setup
├── docker-compose.yml   # Full-stack config
├── .env                 # Environment variables, not included in the portfolio copy
├── .env.production      # Production environment variables, not included in the portfolio copy
├── pytest.ini           # Pytest configuration file
├── requirements.txt     # Python dependencies
├── .gitignore           # Files and folders to ignore in Git version control
├── README.MD            # Project documentation (description, setup instructions)
├── setup.py             # Configuration for packaging the project as a Python package
└── .github/workflows/   # CI/CD pipelines
    └── main.yml         # GitHub Actions workflow
```

---

## **📜 License**
This code is provided for educational purposes only.

## Portfolio Cleanup
Runtime SQLite databases were removed from this copy. Run the initialization step locally to recreate them.
