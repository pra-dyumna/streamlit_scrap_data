# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Optional
# import pandas as pd
# import uvicorn

# from serpapi import search_and_extract
# # Include all your existing scraping functions here (get_driver, search_google, 
# # search_bing, search_duckduckgo, extract_info_from_page, etc.)

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class SearchRequest(BaseModel):
#     query: str
#     location: str = "usa"
#     num_results: int = 10

# class SearchResult(BaseModel):
#     website_url: str
#     phone_number: str
#     email_address: str
#     contact_us: str

# @app.post("/search", response_model=List[SearchResult])
# async def perform_search(request: SearchRequest):
#     try:
#         # Call your existing search_and_extract function
#         df = search_and_extract(
#             query=request.query,
#             location=request.location,
#             num_results=request.num_results
#         )
        
#         # Convert DataFrame to list of dictionaries
#         results = df.to_dict('records')
        
#         # Convert to our response model format
#         formatted_results = []
#         for result in results:
#             formatted_results.append({
#                 "website_url": result.get("Website URL", ""),
#                 "phone_number": result.get("Phone Number", ""),
#                 "email_address": result.get("Email Address", ""),
#                 "contact_us": result.get("Contact Us", "")
#             })
        
#         return formatted_results
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import uvicorn
from serpapi import search_and_extract
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # This allows both GET and POST
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    location: str = "usa"
    num_results: int = 10

class SearchResult(BaseModel):
    website_url: str
    phone_number: Optional[str] = None  # Made optional
    email_address: Optional[str] = None  # Made optional
    contact_us: Optional[str] = None  # Made optional

# Handle POST requests (recommended)
@app.post("/search", response_model=List[SearchResult])
async def perform_search(request: SearchRequest):
    try:
        df = search_and_extract(
            query=request.query,
            location=request.location,
            num_results=request.num_results
        )
        
        # Clean the data before returning
        results = []
        for _, row in df.iterrows():
            results.append({
                "website_url": row.get("Website URL", ""),
                "phone_number": row.get("Phone Number", ""),
                "email_address": row.get("Email Address", ""),
                "contact_us": row.get("Contact Us", "")
            })
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add GET handler if needed (not recommended for search)
@app.get("/search")
async def get_search(query: str, location: str = "usa", num_results: int = 10):
    return await perform_search(SearchRequest(
        query=query,
        location=location,
        num_results=num_results
    ))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)