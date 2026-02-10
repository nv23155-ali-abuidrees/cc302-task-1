# TaskMaster - Task Management Application

A professional task management web application built with Flask and Bootstrap.

## Features

✨ **Core Features:**
- ✅ Create, edit, and delete tasks
- 🌟 Mark tasks as important with visual highlighting
- ✔️ Mark tasks as completed
- 🎨 Professional Bootstrap UI with animations
- 🔄 Real-time task counter

## Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Python 3.12+ (for local development)

## Quick Start with Docker

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

The app will be available at `http://localhost:5000`

### Using Docker CLI

```bash
# Build the image
docker build -t taskmaster:latest .

# Run the container
docker run -p 5000:5000 -v $(pwd)/tasks.db:/app/tasks.db taskmaster:latest
```

## Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cc302-task-1
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python appp.py
   ```

4b. **Alternative: use the provided helper script**
   ```bash
   # make executable and run (from project root)
   chmod +x scripts/run.sh
   ./scripts/run.sh
   ```

5. **Open in browser**
   - Navigate to `http://localhost:5000`

## Project Structure

```
cc302-task-1/
├── appp.py                 # Flask application
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── templates/
│   ├── index.html         # Main task list page
│   └── edit.html          # Task editing page
└── tasks.db               # SQLite database (created at runtime)
```

## API Routes

- `GET /` - View all tasks
- `POST /add` - Add a new task
- `GET /complete/<id>` - Toggle task completion status
- `GET /toggle-important/<id>` - Toggle task importance
- `GET /edit/<id>` - Edit task page
- `POST /edit/<id>` - Save task changes
- `GET /delete/<id>` - Delete a task

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy, SQLite
- **Frontend:** Bootstrap 5, Font Awesome, HTML5, CSS3
- **Containerization:** Docker, Docker Compose
- **Language:** Python 3.12

## Docker Image Details

- **Base Image:** `python:3.12-slim`
- **Port:** 5000
- **Environment:** Production
- **Database:** SQLite (persistent volume)

## Environment Variables

- `FLASK_APP` - Set to `appp.py` (default in container)
- `FLASK_ENV` - Set to `production` (default in container)

## Troubleshooting

**Port already in use:**
```bash
docker-compose down
docker-compose up --build
```

**Database issues:**
```bash
# Remove the database and restart (will create fresh database)
rm tasks.db
docker-compose restart
```

**View container logs:**
```bash
docker-compose logs -f taskmaster
```

## License

This project is open source and available under the MIT License.
