from fastapi import APIRouter

router = APIRouter(prefix="/notes", tags=["consultation_notes"])

@router.get("/")
def notes_removed():
    return {"message": "Notes feature removed for GDPR compliance. All consultation data exists only in your browser and is deleted after export."}

@router.get("/{note_id}")
def note_removed(note_id: int):
    return {"message": "Notes feature removed for GDPR compliance. All consultation data exists only in your browser and is deleted after export."}

@router.post("/")
def create_note_removed():
    return {"message": "Notes feature removed for GDPR compliance. All consultation data exists only in your browser and is deleted after export."}

@router.put("/{note_id}")
def update_note_removed(note_id: int):
    return {"message": "Notes feature removed for GDPR compliance. All consultation data exists only in your browser and is deleted after export."}

@router.delete("/{note_id}")
def delete_note_removed(note_id: int):
    return {"message": "Notes feature removed for GDPR compliance. All consultation data exists only in your browser and is deleted after export."}