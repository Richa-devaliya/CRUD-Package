# Full-Stack CRUD Automation Project

This project provides a complete, production-ready CRUD automation package with a Python/FastAPI backend, a React/Tailwind frontend, and comprehensive deployment instructions for Google Cloud Platform (GCP).

## ✨ Features

-   **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
-   **Frontend**: React (Vite) + Tailwind CSS
-   **Databases**: PostgreSQL (in Docker) & local MongoDB support.
-   **Architecture**: Clean, layered architecture (API -> Services -> Repositories).
-   **DevOps**: Dockerized setup with `docker-compose`.
-   **Deployment**: Detailed step-by-step guide for deploying to GCP Cloud Run, Cloud SQL, and Secret Manager.

## 🚀 Quickstart (Local Development)

### Prerequisites

-   Python 3.11+
-   Poetry (for Python dependency management)
-   Docker & Docker Compose
-   Node.js & npm (or yarn/pnpm)
-   MongoDB installed and running locally (if you plan to use it).

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd crud-automation-project