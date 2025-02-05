from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import format_checker
import disposable
import rolebased
import smtp




import logging

logging.basicConfig(level=logging.INFO)

@app.post("/validate_email/")
def validate_email(request: EmailRequest):
    logging.info(f"Received request: {request.email}")
    return [process_email(email) for email in request.email] if isinstance(request.email, list) else process_email(request.email)


app = FastAPI()

class EmailRequest(BaseModel):
    email: Union[str, List[str]]

@app.post("/validate_email/")
def validate_email(request: EmailRequest):
    if isinstance(request.email, list):
        return [process_email(email) for email in request.email]
    return process_email(request.email)

def process_email(email: str):
    # Check format
    fmt_valid, fmt_message = format_checker.check_format(email)
    if not fmt_valid:
        return {"email": email, "status": "format_invalid", "details": fmt_message}
    
    # Check disposable domain
    if disposable.is_disposable(email):
        return {"email": email, "status": "disposable", "details": "Disposable email"}
    
    # Check role-based email
    if rolebased.is_role_based(email):
        return {"email": email, "status": "role_based", "details": "Role-based email"}
    
    # Perform SMTP validation
    email, smtp_status = smtp.check_email(email)
    return {"email": email, "status": smtp_status, "details": "SMTP check"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
