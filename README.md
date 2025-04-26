# Bayerische Datenwerke

A litigation management system for the automotive industry.

## Problem

Legal professionals in the automotive industry face challenges in efficiently managing large volumes of vehicle-related legal cases, tracking case progress, and identifying trends or recurring issues. Manual processes and fragmented data sources hinder productivity and limit the ability to gain actionable insights from case data.

## Main Features

-   Centralized legal case management for automotive cases
-   Dashboard for case tracking and status overview
-   Advanced analytics and trend visualization
-   Car and part-specific statistics
-   Easy case creation and detailed case views
-   Secure, modern web interface

## Business Value

Bayerische Datenwerke streamlines legal case management for automotive organizations, law firms, and in-house legal teams. By providing a unified platform for case tracking and analytics, it reduces administrative overhead, improves decision-making, and uncovers actionable insights to mitigate legal risks and optimize outcomes. The system empowers legal professionals to work more efficiently and deliver greater value to their clients or organizations.

## Project Overview

Bayerische Datenwerke is a web application designed to manage and analyze legal cases for the automotive industry. It enables legal professionals to efficiently manage and analyze vehicle-related legal cases. Our tool provides an easy-to-use web interface for case tracking, statistical analysis, and visualization of trends in legal cases. The system helps legal professionals manage their caseload efficiently and identify patterns in automotive-related legal issues.

## AI tools used during development

-   v0.dev
-   GitHub Copilot
-   ChatGPT

## Experiments Folder

The `experiments/` directory contains data and notebooks used for downloading and analyzing previous court cases.

-   `bmw_court_cases.json` – Sample dataset of court cases
-   `case_fetcher.ipynb` – Jupyter notebook for fetching previous court cases from the BMW Group.

## Project Architecture

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

5. Create a `.env` file in the backend directory with your Google API key:

    ```
    API_KEY=your_google_api_key_here
    ```

6. Start the backend server:
    ```
    ./start.sh
    ```
    Or manually with:
    ```
    uvicorn main:app --reload --host 0.0.0.0 --port 8000 --env-file .env
    ```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs.

### Frontend Setup

1. Navigate to the frontend directory:

    ```
    cd frontend
    ```

2. Install dependencies:

    ```
    npm install --legacy-peer-deps
    ```

3. Start the development server:
    ```
    npm run dev
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
