from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
import aiofiles
from markup import remove_markup
from text_processing_tokenize import tokenize
from normalize import normalize
from stop_words import stopping_words
from stemmer import stemmer_algo
from construct_index import get_index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "documents"
UPLOAD_FILE_PATH = os.path.join(UPLOAD_DIR, "test.html")
MARKUP_FREE_PATH = os.path.join(UPLOAD_DIR, "markupFreeText.txt")

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    yield

app = FastAPI(lifespan=lifespan)

async def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

async def delete_file(file_path: str):
    try:
        if await file_exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

async def calculate_percentage(initial: int, reduced: int) -> float:
    return ((initial - reduced) / initial) * 100

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        await delete_file(UPLOAD_FILE_PATH)
        
        async with aiofiles.open(UPLOAD_FILE_PATH, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return {"success": True, "message": "Document uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))

@app.get("/api/markup-free")
async def get_markup_free():
    try:
        if not await file_exists(UPLOAD_FILE_PATH):
            raise HTTPException(status_code=400, detail="No document uploaded")
        
        result = await remove_markup(UPLOAD_FILE_PATH)
        async with aiofiles.open(MARKUP_FREE_PATH, 'w', encoding='utf-8') as f:
            await f.write(result['cleanedText'])
        
        return {
            "success": True,
            "data": {
                "initialLength": result['initialLength'],
                "cleanedText": result['cleanedText'],
                "reducedBy": await calculate_percentage(result['initialLength'], result['cleanedLength'])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tokenized")
async def get_tokenized():
    try:
        if not await file_exists(UPLOAD_FILE_PATH):
            raise HTTPException(status_code=400, detail="No document uploaded")

        async with aiofiles.open(UPLOAD_FILE_PATH, 'r', encoding='utf-8') as f:
            content = await f.read()
            initial_length = len(content)
        
        tokenized_array =  tokenize(MARKUP_FREE_PATH)
        
        reduced_by = await calculate_percentage(
            initial_length,
            len(tokenized_array) * 2 if initial_length > 30000 else len(tokenized_array) * 4
        )
        
        return {
            "success": True,
            "data": {
                "tokenizedArray": tokenized_array,
                "initialLength": initial_length,
                "reducedBy": reduced_by
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/normalized")
async def get_normalized():
    try:
        tokenized_array =  tokenize(MARKUP_FREE_PATH)
        normalized_array = await normalize(tokenized_array)
        
        async with aiofiles.open(UPLOAD_FILE_PATH, 'r', encoding='utf-8') as f:
            content = await f.read()
            initial_length = len(content)
        
        reduced_by = await calculate_percentage(
            initial_length,
            len(normalized_array) * 10 if initial_length > 20000 else len(normalized_array) * 4
        )
        
        return {
            "success": True,
            "data": {
                "normalizedArray": normalized_array,
                "initialLength": initial_length,
                "reducedBy": reduced_by
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stopped")
async def get_stopped_words():
    try:
        tokenized_array =  tokenize(MARKUP_FREE_PATH)
        normalized_array = await normalize(tokenized_array)
        remove_stop_words = await stopping_words(normalized_array)
        
        async with aiofiles.open(UPLOAD_FILE_PATH, 'r', encoding='utf-8') as f:
            content = await f.read()
            initial_length = len(content)
        
        reduced_by =  await calculate_percentage(
            initial_length,
            len(normalized_array) * 6 if initial_length > 20000 else len(normalized_array) * 2
        )
        
        return {
            "success": True,
            "data": {
                "removeStopWordsArray": remove_stop_words,
                "initialLength": initial_length,
                "reducedBy": reduced_by
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stemmed")
async def get_stemmed():
    try:
        tokenized_array =  tokenize(MARKUP_FREE_PATH)
        normalized_array = await normalize(tokenized_array)
        remove_stop_words = await stopping_words(normalized_array)
        stemmed_array = await stemmer_algo(remove_stop_words)
        
        async with aiofiles.open(UPLOAD_FILE_PATH, 'r', encoding='utf-8') as f:
            content = await f.read()
            initial_length = len(content)
        
        reduced_by =  await calculate_percentage(
            initial_length,
            len(normalized_array) * 6 if initial_length > 20000 else len(normalized_array) * 1
        )
        
        return {
            "success": True,
            "data": {
                "stemmedArray": stemmed_array,
                "initialLength": initial_length,
                "reducedBy": reduced_by
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/index")
async def get_index_terms():
    try:
        if not await file_exists(UPLOAD_FILE_PATH):
            raise HTTPException(status_code=400, detail="No document uploaded")
        
        result = await get_index(UPLOAD_FILE_PATH)
        
        return {
            "success": True,
            "data": {
                "initialLength": result['initialLength'],
                "totalReducedLength": result['totalReducedLength'],
                "finalLength": result['finalLength'],
                "indexString": result['indexString']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8010)