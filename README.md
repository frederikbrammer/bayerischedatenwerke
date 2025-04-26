# Bayerische Datenwerke

A legal case management system with analytics capabilities for vehicle-related legal cases.

## Project Overview

Bayerische Datenwerke is a web application designed to manage and analyze legal cases for the automotive industry. It provides a modern interface for case tracking, statistical analysis, and visualization of trends in legal cases. The system helps legal professionals manage their caseload efficiently and identify patterns in automotive-related legal issues.

## Project Architecture

The project follows a modern client-server architecture:

### Backend (FastAPI)

-   **Framework**: FastAPI (Python-based)
-   **Directory Structure**:
    -   `main.py` - Application entry point and server configuration
    -   `app/` - Core application modules
        -   `db/` - Database interactions and JSON data storage
        -   `models/` - Data models and schemas
        -   `routers/` - API endpoints (cases and statistics)
    -   `requirements.txt` - Python dependencies

### Frontend (Next.js)

-   **Framework**: Next.js with TypeScript and React
-   **Directory Structure**:
    -   `app/` - Next.js app router pages
        -   `cases/` - Case management views
        -   `trends/` - Statistical analysis views
    -   `components/` - Reusable UI components
        -   `charts/` - Data visualization components
        -   `ui/` - General UI components (buttons, cards, etc.)
    -   `lib/` - Utility functions and API client
    -   `public/` - Static assets
    -   `styles/` - Global CSS styles

### Key Features

-   Case management dashboard
-   Legal case creation and viewing
-   Statistical analysis and trend visualization
-   Car and part-specific analytics
-   Case status tracking

## Setup and Running the Project

### Prerequisites

-   Python 3.13+
-   Node.js (latest LTS recommended)
-   pnpm package manager

### Backend Setup

1. Navigate to the backend directory:

    ```
    cd backend
    ```

2. Create a virtual environment (if not already present):

    ```
    python -m venv env
    ```

3. Activate the virtual environment:

    - macOS/Linux: `source env/bin/activate`
    - Windows: `.\env\Scripts\activate`

4. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

5. Start the backend server:
    ```
    ./start.sh
    ```
    Or manually with:
    ```
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs.

### Frontend Setup

1. Navigate to the frontend directory:

    ```
    cd frontend
    ```

2. Install dependencies:

    ```
    pnpm install
    ```

3. Start the development server:
    ```
    pnpm dev
    ```

The application will be available at http://localhost:3000.

## API Endpoints

-   `GET /api/cases/` - List all cases
-   `GET /api/cases/{id}` - Get a specific case
-   `POST /api/cases/` - Create a new case
-   `GET /api/stats/` - Get general statistics
-   `GET /api/stats/cars` - Get car-related statistics
-   `GET /api/stats/parts` - Get part-related statistics
-   `GET /api/stats/status` - Get case status statistics
