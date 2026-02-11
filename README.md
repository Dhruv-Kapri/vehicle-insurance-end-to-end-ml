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

- **Project scaffolding & packaging** using `pyproject.toml`
- **Centralized logging** module
- **Custom exception handling**
- **MongoDB Atlas setup & connection**
- **EDA & Feature Engineering** notebook
- **Data Ingestion pipeline**
  - MongoDB → `pandas.DataFrame`
  - Train / Test split
  - Artifact generation
- **Data Validation**
  - Schema-based column validation
  - Numerical & categorical column checks
  - Validation report generation
- **Data Transformation**
  - Custom feature engineering
  - Scaling via `ColumnTransformer`
  - Class imbalance handling using **SMOTEENN**
  - Transformation object persistence
- **Model Trainer**
  - Trains a Random Forest model using transformed datasets, pre-selected hyper-parameters
  - Handle class imbalance–aware training data
  - Perform model fitting with configurable hyperparameters
  - Checks model accuracy across a predefined threshold
  - Save trained model artifacts for downstream evaluation & deployment
- **Model Evaluation**
  - Compares newly trained model against production model (if exists)
  - Computes F1-score on holdout test dataset
  - Accepts model only if performance improves
  - Generates model comparison artifact
  - Ensures safe model version promotion
- **Model Pusher** (AWS S3)
  - Uploads accepted model to AWS S3 bucket
  - Maintains production model path
  - Enables model version control via cloud storage

### Upcoming

- **Prediction Pipeline**
- **CI/CD** with GitHub Actions
- **Deployment** on AWS EC2

---

## Workflow Components

### 1. Data Ingestion Workflow

The **Data Ingestion component** performs the following steps:

1. Connects to **MongoDB Atlas** using environment variables
2. Fetches raw data from the target collection
3. Converts MongoDB documents into a `pandas.DataFrame`
4. Stores raw data in the **feature store**
5. Splits data into **train** and **test** sets
6. Saves ingested datasets as **artifacts**
7. Logs each step and handles failures gracefully

#### Artifacts generated:

```text
artifact/<timestamp>/data_ingestion/
├── feature_store/
│   └── data.csv
└── ingested/
    ├── train.csv
    └── test.csv
```

### 2. Data Validation Workflow

The **Data Validation component** ensures that ingested data strictly conforms to the schema defined in `schema.yaml`.

#### Validations Performed:

1. Validates **number of columns** against schema
2. Verifies presence of all **numerical columns**
3. Verifies presence of all **categorical columns**
4. Aggregates validation errors into a report
5. Blocks pipeline execution if validation fails

#### Artifacts generated:

```text
artifact/<timestamp>/data_validation/
└── report.yaml
```

### 3. Data Transformation Workflow

The **Data Transformation component** prepares data for model training using a combination of custom logic and sklearn pipelines.

#### Steps:

1. Loads validated train & test datasets
2. Separates input features and target column
3. Applies custom transformations:
   - Gender mapping (`Female → 0`, `Male → 1`)
   - ID column removal
   - One-hot encoding for categorical features
   - Column renaming & type casting
4. Applies scaling using ColumnTransformer:
   - `StandardScaler` for numerical features
   - `MinMaxScaler` for selected columns
5. Handles class imbalance using **SMOTEENN**
6. Concatenates transformed features with target labels
7. Saves transformation artifacts

#### Artifacts generated:

```text
artifact/<timestamp>/data_transformation/
├── transformed/
│   ├── train.npy
│   └── test.npy
└── transformed_object/
    └── proprocessing.pkl
```

### 4. Model Trainer Workflow

The **Model Trainer component** is responsible for training, and persisting the ML model using the transformed datasets produced by the **Data Transformation component** in the pipeline.

#### Steps:

1. Loads transformed train & test arrays (`.npy`)
2. Splits arrays into:
   - Input features (`X`)
   - Target labels (`y`)
3. Trains `Random Forest` models and evaluates if it's accuracy is greater than set threshold
4. Evaluates models using appropriate classification metrics
5. Persists the trained model as an artifact
6. Logs training metrics and model selection details

#### Artifacts generated:

```text
artifact/<timestamp>/model_trainer/trained_model
└── model.pkl
```

### 5. Model Evaluation Workflow

The **Model Evaluation component** is responsible for validating whether the newly trained model should replace the current production model.

#### Steps:

1. Loads holdout **test dataset**
2. Applies identical preprocessing logic used during training
3. Loads newly trained model artifact
4. Fetches production model from **AWS S3** (if available)
5. Computes **F1-score** for:
   - Newly trained model
   - Production model
6. Compares performance difference
7. Accepts model only if performance improves

### 6. Model Pusher Workflow

The **Model Pusher component** is responsible for promoting the accepted model to production by uploading it to AWS S3.

#### Steps:

1. Checks if model is approved by Model Evaluation stage
2. Uploads trained model to configured **S3 bucket**
3. Overwrites or versions production model path
4. Generates model pusher artifact

#### Artifacts generated:

```text
aws/Amazon S3/Buckets/vehicle-insurance-s3-bucket
└── model.pkl
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
AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
```

### Option 2: Export directly (Linux / macOS)

```bash
export MONGODB_CONNECTION_URL="mongodb+srv://<username>:<password>@<cluster-url>"
export AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"
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

- **Language:** Python `3.12`
- **ML:** `Scikit-learn`, `Pandas`, `NumPy`
- **Database:** MongoDB Atlas
- **MLOps:** Docker, AWS S3, GitHub Actions _(planned)_
- **Backend:** FastAPI / Flask _(planned)_
- **Deployment:** AWS EC2 _(planned)_

---

## License

MIT License
