# Patient Management System API
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-orange)
![Pydantic](https://img.shields.io/badge/Pydantic-latest-green)
![Uvicorn](https://img.shields.io/badge/Uvicorn-latest-red)

A fully functional RESTful API built with FastAPI to manage patient records, including creating, reading, updating, and deleting patient data stored in a JSON file. The API supports patient data validation, BMI calculation, and sorting capabilities.

## Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Usage](#example-usage)
- [Data Storage](#data-storage)
- [Notes](#notes)
- [Support](#support)

## Project Overview
The Patient Management System API allows users to manage patient records, including details such as ID, name, city, age, gender, height, and weight. It automatically calculates the patient's BMI and categorizes their weight status (underweight, normal, or obese). The API uses a JSON file (`patients.json`) as its data store and provides endpoints for CRUD operations (Create, Read, Update, Delete) and sorting patient records by height, weight, or BMI.

## 📂 Project Structure

```text
PATIENT-MANAGEMENT-SYSTEM/
├── __pycache__/          # Python compiled bytecode
├── app/                  # Core application
│   ├── crud.py           # Database operations
│   ├── main.py           # FastAPI initialization
│   ├── models.py         # Data models and validations
│   └── routes.py         # API endpoint definitions
├── myenv/                # Python virtual environment
├── .gitignore            # Version control ignore rules
├── LICENSE               # MIT License
├── patients.json         # Patient database (auto-created)
├── README.md             # This documentation
└── requirements.txt      # Python dependencies

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Uvicorn (ASGI server for running FastAPI)
- Required Python packages:
  - `fastapi`
  - `pydantic`
  - `uvicorn`

## Installation
1. Clone the repository or copy the project files to your local machine.
2. Navigate to the project directory:
   ```bash
   cd patient_management
   ```
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install fastapi pydantic uvicorn
   ```

## Running the Application
1. Ensure you are in the `patient_management` directory.
2. Run the FastAPI application using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   The `--reload` flag enables auto-reload for development.
3. The API will be available at `http://127.0.0.1:8000`.
4. Access the interactive API documentation at `http://127.0.0.1:8000/docs` (provided by FastAPI's Swagger UI).

## API Endpoints
The API provides the following endpoints for managing patient records:

| Method | Endpoint                  | Description                                      | Parameters/Body                                                                 |
|--------|---------------------------|--------------------------------------------------|---------------------------------------------------------------------------------|
| GET    | `/`                       | Returns a welcome message                        | None                                                                            |
| GET    | `/about`                  | Returns a description of the API                 | None                                                                            |
| GET    | `/view`                   | Retrieves all patient records                    | None                                                                            |
| GET    | `/patient/{patient_id}`   | Retrieves a specific patient by ID               | Path: `patient_id` (e.g., `p001`)                                               |
| GET    | `/sort`                   | Sorts patients by height, weight, or BMI         | Query: `sort_by` (height, weight, bmi), `order` (asc, desc, default: asc)       |
| POST   | `/create`                 | Creates a new patient record                     | Body: JSON with `id`, `name`, `city`, `age`, `gender`, `height`, `weight`       |
| PUT    | `/edit/{patient_id}`      | Updates an existing patient record               | Path: `patient_id`, Body: JSON with optional fields to update                    |
| DELETE | `/delete/{patient_id}`    | Deletes a patient record by ID                   | Path: `patient_id`                                                              |

### Patient Data Schema
- **id**: String, unique identifier (e.g., `P001`)
- **name**: String, patient's name
- **city**: String, patient's city
- **age**: Integer, patient's age (1–119)
- **gender**: String, one of `male`, `female`, or `others`
- **height**: Float, patient's height in meters (>0)
- **weight**: Float, patient's weight in kilograms (>0)
- **bmi**: Float, computed as `weight / (height^2)`, rounded to 2 decimal places
- **verdict**: String, computed as `underweight` (BMI < 18.5), `Normal` (18.5 ≤ BMI < 25), or `obese` (BMI ≥ 25)

## Example Usage
### Create a Patient
```bash
curl -X POST "http://127.0.0.1:8000/create" -H "Content-Type: application/json" -d '{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.0
}'
```
**Response**: `201 Created` with `"Patient created successfully"`

### View a Patient
```bash
curl "http://127.0.0.1:8000/patient/P001"
```
**Response**:
```json
{
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.0,
  "bmi": 22.86,
  "verdict": "Normal"
}
```

### Sort Patients by BMI
```bash
curl "http://127.0.0.1:8000/sort?sort_by=bmi&order=desc"
```
**Response**: Array of patient records sorted by BMI in descending order.

## Data Storage
- Patient data is stored in a `patients.json` file in the project root directory.
- The file is automatically created/updated when you create, update, or delete patients.
- Ensure the application has write permissions in the directory to modify `patients.json`.

## Notes
- The API uses a JSON file for simplicity. For production, consider using a database like PostgreSQL or MongoDB for better performance and scalability.
- The `/sort` endpoint uses a `key` function in Python's `sorted` method to sort patients. The `lambda x: x.get(sort_by, 0)` extracts the value of the specified field (e.g., `height`, `weight`, `bmi`) for sorting, defaulting to 0 if the field is missing.
- All patient IDs are case-insensitive (converted to uppercase internally).
- The API validates input data using Pydantic models, ensuring fields like `age`, `height`, and `weight` meet specified constraints.

## Support
For issues or questions, please contact the project maintainer or open an issue on the repository (if hosted on a platform like GitHub). Contributions and feedback are welcome!
