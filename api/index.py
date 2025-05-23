# api/index.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET"], 
    allow_headers=["*"],  
)

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-python.json')

df_marks = pd.DataFrame(columns=['name', 'marks']) 
print(f"Attempting to load data from: {JSON_FILE_PATH}")
if not os.path.exists(JSON_FILE_PATH):
    print(f"Error: JSON file NOT found at {JSON_FILE_PATH}")
else:
    try:
        df_marks = pd.read_json(JSON_FILE_PATH)
        print(f"Successfully loaded data. DataFrame head:\n{df_marks.head()}")
        print(f"DataFrame columns: {df_marks.columns.tolist()}")
    except Exception as e:
        print(f"An error occurred while loading JSON: {e}")


@app.get("/api")
async def get_student_marks(name: list[str] = Query(None)):
    print(f"Received API request for names: {name}")
    if not name:
        print("No names provided in query, returning empty list.")
        return {"marks": []}
    results = []
    for student_name_raw in name:
        search_name = student_name_raw.strip('"')
        print(f"Searching for student (direct match): '{search_name}' (from raw: '{student_name_raw}')")
        if 'name' in df_marks.columns: 
            mark_series = df_marks[df_marks['name'] == search_name]['marks'] 
            print(f"Here's the mark_series for {search_name}: {mark_series}")
            if not mark_series.empty:
                mark = mark_series.iloc[0] 
                try:
                    results.append(int(mark))
                    print(f"Found mark {mark} for '{student_name_raw}'")
                except ValueError:
                    print(f"Warning: Mark for '{student_name_raw}' is not a valid integer: {mark}")
            else:
                print(f"Warning: Mark not found for student: '{student_name_raw}'")
        else:
            print("Error: 'name' column not found in DataFrame. Data not loaded correctly.")
            break

    print(f"Final results to return: {results}")
    return {"marks": results}
