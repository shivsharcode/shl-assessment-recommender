# SHL Assessment Recommendation System

This project is a recommendation system for SHL assessments. It uses a combination of web crawling, vectorization, and a backend API to recommend assessments based on user queries. The system is built using Python, FastAPI, and machine learning models for semantic search.


## LINKS


#### BACKEND API ENDPOINTS  (hosted on render)
1. activate : https://shl-backend-api-1.onrender.com/
2. health : https://shl-backend-api-1.onrender.com/health
3. recommend : https://shl-backend-api-1.onrender.com/recommend

#### DEMO FRONTEND WORKING -- CONNECTED WITH BACKEND API
Link : https://shl-assignment-shivamsharma.streamlit.app/

<!-- 
## GUIDE THROUGH THE PROJECT
1. git clone https://github.com/shivsharcode/shl-assessment-recommender.git
2. cd shl-assessment-recommender
3. Install dependencies: pip install requirements.txt
4. Activate Backend (locally hosted here, but the api link hosted on render is also given)
5. cd 4.BACKEND-API
6. uvicorn main:app --reload
7. Open a new terminal in the shl-assessment-recommender folder
8. Start Frontend
9. streamlit run app_streamlit.py
 -->

---

## 🚀 Project Setup Guide: SHL Assessment Recommender

Follow the steps below to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/shivsharcode/shl-assessment-recommender.git
cd shl-assessment-recommender
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Backend API

The backend is hosted locally, but you can also use the production version hosted on Render.

To run the backend locally:

```bash
cd 4.BACKEND-API
uvicorn main:app --reload
```

### 4. Start the Frontend

In a **new terminal**, return to the root project directory:

```bash
cd ..
streamlit run app_streamlit.py
```

---

### 🔗 Note

Render may put the backend API to sleep after periods of inactivity.
Before clicking **Recommend**, visit this URL once to wake the API:

[https://shl-backend-api-1.onrender.com/](https://shl-backend-api-1.onrender.com/)

---




## Project Structure

The project is organized into the following directories:

### 1. Web Crawler
- **Purpose**: Crawls SHL's website to collect assessment data.
<!-- - **Key File**: `shl_assessments_complete.json`
  - Contains details of assessments such as name, URL, description, duration, and test types. -->

### 2. Vectorization
- **Purpose**: Converts assessment descriptions into vector embeddings for semantic search.
<!-- - **Key Files**:
  - `shl_assessments_complete.json`: Input data for vectorization.
  - `shl_index_metadata.json`: Metadata for the vectorized index.
  - `shl_index.faiss`: FAISS index for fast similarity search. -->

### 3. Evaluation
- **Purpose**: Evaluates the performance of the recommendation system.
<!-- - **Key Files**:
  - `shl_assessments_complete.json`: Assessment data for evaluation.
  - `shl_index_metadata.json`: Metadata for evaluation. -->

### 4. Backend API
- **Purpose**: Provides an API for querying the recommendation system.
<!-- - **Key Files**:
  - `main.py`: FastAPI application that handles requests and returns recommendations.
  - `shl_index_metadata.json`: Metadata used by the API. -->


## Key Features

1. **Web Crawling**: Extracts assessment data from SHL's website.
2. **Vectorization**: Uses `SentenceTransformer` to generate embeddings for semantic search.
3. **Recommendation API**: Provides endpoints to query assessments based on user input.
4. **Evaluation**: Measures the accuracy and performance of the recommendation system.

## API Endpoints

### Base URL
`https://shl-backend-api-1.onrender.com/`

### Endpoints
- **`GET /`**: Returns a welcome message.
- **`GET /health`**: Returns the health status of the API.
- **`POST /recommend`**: Accepts a query and returns a list of recommended assessments.

#### Example Request
```json
POST /recommend
{
  "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes"
}
```
#### Example Response
```json
{
  "results": [
    {
      "url": "https://www.shl.com/products/product-catalog/view/python-new/",
      "adaptive_support": "No",
      "description": "Multi-choice test that measures the knowledge of Python programming, databases, modules and library.",
      "duration": 11,
      "remote_support": "Yes",
      "test_types": ["Knowledge & Skills"]
    }
  ]
}
```



