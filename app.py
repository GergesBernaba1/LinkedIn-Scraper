from fastapi import FastAPI, Query, HTTPException
from googlesearch import search
from typing import List
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/search")
def search_linkedin(
    job_title: str = Query(..., description="Job title to search"),
    location: str = Query(..., description="Location to search"),
    years_experience: int = Query(None, description="Minimum years of experience required"),
    limit: int = Query(10, description="Number of results to return")
):
    try:
        # Base query with job title and location
        query = f'site:linkedin.com/in/ "{job_title}" "{location}"'
        
        # Add years of experience to the query if specified
        if years_experience:
            query += f' "{years_experience}+ years"'
        
        logger.info(f"Searching with query: {query}")
        results = []

        for url in search(query, num_results=limit):
            if "linkedin.com/in/" in url:
                results.append({
                    "linkedin_url": url
                })

        logger.info(f"Found {len(results)} results")
        return {"results": results}
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Run using: uvicorn linkedin_api:app --reload
if __name__ == "__main__":
    uvicorn.run("linkedin_api:app", host="0.0.0.0", port=8000, reload=True)
