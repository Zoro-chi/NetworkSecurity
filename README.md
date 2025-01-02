### Network Security Project for Phishing Detection

This project focuses on network security by leveraging machine learning and data science techniques to detect phishing attacks. The project involves data ingestion, validation, transformation, and model training to build a robust phishing detection system.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Data Ingestion](#data-ingestion)
- [Data Validation](#data-validation)
- [Data Transformation](#data-transformation)
- [Model Training](#model-training)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project focuses on network security by leveraging machine learning and data science techniques to detect phishing attacks. The project involves data ingestion, validation, transformation, and model training to build a robust phishing detection system.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/NetworkSecurity.git
   cd NetworkSecurity
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the necessary environment variables set up. You can use a [.env](http://_vscodecontentref_/4) file for this purpose.
2. Run the main script:
   ```sh
   python main.py
   ```

## Configuration

Configuration settings are defined in the `network_security/constants/training_pipeline.py` file. You can adjust the settings for data ingestion, validation, transformation, and model training as needed.

## Data Ingestion

The data ingestion component reads data from a MongoDB collection and exports it as a DataFrame. The data is then split into training and testing sets.

## Data Validation

The data validation component checks the number of columns and detects data drift between the training and testing datasets. It generates a drift report saved in the `artifacts` directory.

## Data Transformation

The data transformation component handles missing values using KNN imputation and transforms the data into a suitable format for model training.

## Model Training

The model training component trains a machine learning model using the transformed data. The trained model is saved in the `artifacts` directory.

## Results

The results of the data ingestion, validation, transformation, and model training processes are saved in the `artifacts` directory. You can review the generated reports and trained models.
