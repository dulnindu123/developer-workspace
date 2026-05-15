from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import models, schemas, auth, ast_parser
from database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Developer Workspace API")

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, name=user.name, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_project = models.Project(**project.model_dump(), owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

from fastapi import UploadFile, File

@app.post("/projects/{project_id}/analyze", response_model=schemas.ArchitectureGraph)
async def analyze_project_file(project_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Read file content
    content = await file.read()
    code_str = content.decode("utf-8")
    
    # Update status to analyzing (for synchronous visibility)
    project.status = "analyzing"
    db.commit()
    
    # Run Parser
    classes, functions, dependencies = ast_parser.analyze_code(code_str, project.language)
    
    # Save to DB
    for cls in classes:
        db.add(models.ClassNode(project_id=project.id, file_path=file.filename, **cls))
    for func in functions:
        db.add(models.FunctionNode(project_id=project.id, file_path=file.filename, **func))
    for dep in dependencies:
        db.add(models.DependencyEdge(project_id=project.id, **dep))
        
    project.status = "completed"
    db.commit()
    
    # Return architecture graph
    return {
        "classes": db.query(models.ClassNode).filter(models.ClassNode.project_id == project_id).all(),
        "functions": db.query(models.FunctionNode).filter(models.FunctionNode.project_id == project_id).all(),
        "dependencies": db.query(models.DependencyEdge).filter(models.DependencyEdge.project_id == project_id).all()
    }

