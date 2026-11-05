# MyTaiga Management
helper to manage and pipeline activities data after data mapping

## Requirements
- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-started/get-docker/)
- Docker Compose (Docker Compose Plugin)
- Python 3.12.12 (application runtime) // if run without docker

## Getting Started
```bash
git clone [git@github.com:ludyhasby/mytaiga-management.git](https://github.com/ludyhasby/mytaiga-management.git)
```
```bash
cd mytaiga-management
```
```
cp .env.example .env
```
```bash
docker compose up --build -d
```

or (without docker)
```
streamlit run app.py
```

notes: check docker container ps // port must be fill

after container has been ran, open the browser and access:
```text
http://localhost:8501
```
Enter your my taiga management secret key that set on env

### View Application Logs

to view app log: 
```bash
docker compose logs -f
```

## WebApps Notes
The application is also available through Web Apps.
To access the application, open the following URL in your browser: [MyTaiga-Management](https://mytaiga-management.streamlit.app/)