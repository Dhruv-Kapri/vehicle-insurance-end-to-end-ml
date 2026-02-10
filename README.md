# Vehicle-Insurance-End-to-End-ML

An **end-to-end Machine Learning project** demonstrating a **production-grade ML pipeline** — from **data ingestion using MongoDB** to **model training, evaluation, deployment, and CI/CD using Docker and AWS**.

This project follows an **industry-aligned MLOps workflow** with **modular**, **scalable**, and **maintainable** code architecture.

---

## Project Structure

```bash
Vehicle-Insurance-End-to-End-ML
├── artifact/                     # Generated artifacts (ignored in git)
├── backend/                      # FastAPI/Flask app entry points
├── config/                       # YAML configs (schema, model)
├── frontend/                     # UI (to be added)
├── logs/                         # Application logs
├── notebook/                     # EDA & experimentation notebooks
├── src/                          # Core source code
│   ├── cloud_storage/            # AWS S3 integration
│   ├── components/               # ML pipeline components
│   ├── configuration/            # DB & cloud connections
│   ├── constants/                # Global constants
│   ├── data_access/              # MongoDB data access layer
│   ├── entity/                   # Config & artifact dataclasses
│   ├── exception/                # Custom exception handling
│   ├── logger/                   # Centralized logging
│   ├── pipeline/                 # Training & prediction pipelines
│   └── utils/                    # Utility functions
├── template.py                   # Project scaffolding script
├── Dockerfile                    # Docker configuration
├── pyproject.toml                # Local package setup
├── requirements.txt              # Python dependencies
└── README.md
```

---

## Current Project Status

### Completed

- **Project scaffolding & packaging** using ``pyproject.toml``
- **Centralized logging** module
- **Custom exception handling**
- **MongoDB Atlas setup & connection**
- **EDA & Feature Engineering** notebook
- **Data Ingestion pipeline**
  - MongoDB data fetch
  - Document → ``pandas.DataFrame`` conversion
  - Train / Test split
  - Feature store creation
  - Artifact generation

### Upcoming

- **Data Validation**
- **Data Transformation**
- **Model Trainer**
- **Model Evaluation**
- **Model Pusher** (AWS S3)
- **Prediction Pipeline**
- **CI/CD** with GitHub Actions
- **Deployment** on AWS EC2

---

## Data Ingestion Workflow

The **Data Ingestion component** performs the following steps:

1. Connects to **MongoDB Atlas** using environment variables
2. Fetches raw data from the target collection
3. Converts MongoDB documents into a ``pandas.DataFrame``
4. Stores raw data in the **feature store**
5. Splits data into **train** and **test** sets
6. Saves ingested datasets as **artifacts**
7. Logs each step and handles failures gracefully

### Artifacts generated:

```text
artifact/<timestamp>/data_ingestion/
├── feature_store/
│   └── data.csv
└── ingested/
    ├── train.csv
    └── test.csv
```

---

## Environment Variables

### Option 1: Using `.env` file

```bash
cp .env.example .env
```

Or Create a `.env` file:

```env
MONGODB_CONNECTION_URL=mongodb+srv://<username>:<password>@<cluster-url>
```

### Option 2: Export directly (Linux / macOS)

```bash
export MONGODB_CONNECTION_URL="mongodb+srv://<username>:<password>@<cluster-url>"
```

---

## How to Run (Current Stage)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run data ingestion
python backend/demo.py
```

---

## Tech Stack


- **Language:** Python ``3.12``
- **ML:** ``Scikit-learn``, ``Pandas``, ``NumPy``
- **Database:** MongoDB Atlas
- **MLOps:** Docker, AWS S3, GitHub Actions *(planned)*
- **Backend:** FastAPI / Flask *(planned)*
- **Deployment:** AWS EC2 *(planned)*

---

## License

MIT License
