from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.elevenlabs_routes import router as elevenlabs_router
from app.api.outbound_routes import router as outbound_router
from app.api.evaluation_routes import router as evaluation_router

app=FastAPI(title='RescueVoice API',version='1.2.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(router,prefix='/api')
app.include_router(elevenlabs_router,prefix='/api/elevenlabs',tags=['elevenlabs'])
app.include_router(outbound_router,prefix='/api/elevenlabs',tags=['elevenlabs'])
app.include_router(outbound_router,prefix='/api',tags=['outbound'])
app.include_router(evaluation_router,prefix='/api/evaluation',tags=['evaluation'])
