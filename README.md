# Rhombus AI Data Processor

This project is a web application designed to process and display data, focusing on data type inference and conversion for datasets using Python (Pandas) and ReactJS.

## Project Structure

- `backend/`: Django project for the API and data processing logic.
- `frontend/`: ReactJS application for the user interface.

## Features

- **File Upload:** Users can upload CSV or Excel files.
- **Data Type Inference:** The backend (Django + Pandas) infers appropriate data types for each column in the uploaded dataset.
- **Data Type Mapping:** Pandas data types are mapped to user-friendly names (e.g., 'object' to 'Text', 'datetime64' to 'Date').
- **Data Preview:** Displays a preview of the processed data.
- **Type Override (Frontend):** Provides a basic interface for users to see inferred types and conceptually "override" them (though this version doesn't send overrides back to the backend for actual reprocessing).

## Setup and Running the Application

### Prerequisites

- Python 3.8+
- Node.js (LTS recommended)
- npm or yarn

### 1. Backend Setup (Django)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    -   On Windows: `.\venv\Scripts\activate`
    -   On macOS/Linux: `source venv/bin/activate`
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Create `requirements.txt` manually if not already present, with `django`, `djangorestframework`, `pandas`, `openpyxl`, `numpy`, `django-cors-headers`)
    ```
    # backend/requirements.txt
    Django==4.2.1
    djangorestframework==3.14.0
    pandas==2.0.3
    openpyxl==3.1.2 # Required for Excel file handling
    numpy==1.25.2
    django-cors-headers==4.0.0
    ```
5.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations data_processing
    python manage.py migrate
    ```
6.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```
    The backend API will be available at `http://localhost:8000`.

### 2. Frontend Setup (ReactJS)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install # or yarn install
    ```
3.  **Start the React development server:**
    ```bash
    npm start # or yarn start
    ```
    The React app will typically open in your browser at `http://localhost:3000`.

## Usage

1.  Ensure both the Django backend and React frontend are running.
2.  Open your browser to `http://localhost:3000`.
3.  Use the "Upload Data File" section to select a CSV or Excel file.
4.  Click "Upload and Process" to send the file to the backend.
5.  The processed data preview and inferred data types will be displayed.
6.  You can see the inferred types and conceptually select different "user-friendly" types using the dropdowns (note: this does not re-process data in this minimum version).

## Error Handling and Validations

-   **Backend:** Includes basic error handling for file uploads and data processing errors.
-   **Frontend:** Provides visual feedback for loading states and errors during file upload.

## Notes

-   The data type inference in `data_inference.py` is a starting point and aims for high accuracy but might require further refinement for highly diverse datasets.
-   For large files, asynchronous processing (e.g., using Celery with Redis/RabbitMQ) for the Pandas script would be recommended to prevent frontend timeouts. This is not implemented in this bare-minimum version.
-   The "override" functionality in the frontend is a visual representation; in a production app, this would trigger re-processing or saving user-defined type mappings.
-   Thorough testing with various CSV and Excel files is crucial.
