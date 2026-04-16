from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate,PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

import shutil
import os
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()   # Create  DB tables for us
    yield


app = FastAPI(lifespan=lifespan)




@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        session: AsyncSession = Depends(get_async_session) 
):

    temp_file_path = None
    # Create a temp file to store the uploaded file temporarily before uploading to imagekit
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file: #temp files ends in the filename
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        
        upload_result = imagekit.upload_file(

            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )


        if  upload_result.response.http_status_code == 200:


            post = Post(
                caption=caption,
                url="url",
                file_type="photo",
                file_name=file.filename
            )

        session.add(post)
        await session.commit() # add post to database and commit the transaction
        await session.refresh(post) # refresh the post instance to get the generated ID
        return post
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   # if any error occurs during file upload or database operations, we catch the exception and return a 500 Internal Server Error response with the error message. This helps in debugging and provides feedback to the client about what went wrong.

    finally:   # clean up temp file and close the uploaded file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)

):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()] # all result from upper quesry as we convert into list
    posts_data = []

    for post in posts:
        posts_data.append(
            {
            "id": str(post.id),
            "caption": post.caption,
            "url" : post.url,
            "file_type" : post.file_type,
            "file_name" : post.file_name,
            "created_at" : post.created_at.isoformat()
            }
        )
    return{"posts": posts_data}