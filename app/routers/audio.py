import os
import tempfile
import re
from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Depends
from app.services.pipeline import AudioLensPipeline
from app.models.schema import AudioUploadResponse
from app.db.queries import save_summary
from app.db.supabase import supabase
from app.dependencies import get_current_user

router = APIRouter(prefix="/audio", tags=["audio"])
pipeline = AudioLensPipeline()

SUPPORTED_FORMATS = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
):
    filename = file.filename or ""
    if not any(filename.endswith(ext) for ext in SUPPORTED_FORMATS):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format. Supported: {', '.join(SUPPORTED_FORMATS)}"
        )

    tmp_path = None  

    try:
        suffix = os.path.splitext(filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        result = pipeline.run(tmp_path)

        title = filename.rsplit('.', 1)[0].replace('_', ' ').title() if filename else "Untitled Lecture"
        
        # Split the summary into a list of non-empty lines
        lines = [line.strip() for line in result["summary"].splitlines() if line.strip()]
        
        for i, line in enumerate(lines):
            if "Lecture Title" in line:
                # Case 1: AI put the title on the SAME line 
                cleaned_line = re.sub(r"^.*?Lecture Title[\s:\-*]*", "", line, flags=re.IGNORECASE).strip()
                if cleaned_line and not cleaned_line.startswith("#"):
                    title = cleaned_line
                    break
                
                # Case 2: AI put the title on the NEXT line 
                if i + 1 < len(lines):
                    next_line = lines[i+1]
                    # Make sure it didn't accidentally jump to the next section heading
                    if not next_line.startswith("#"):
                        title = next_line.replace("**", "").replace("*", "").strip()
                        break
       

        saved = save_summary(
            user_id=user_id,
            title=title,
            transcript=result["transcript"],
            summary=result["summary"],
            topics=result["topics"],
            resources=result["resources"],
        )

        return AudioUploadResponse(
            message="Audio processed successfully",
            summary_id=saved["id"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

    finally:
        if tmp_path and os.path.exists(tmp_path):  
            os.remove(tmp_path)