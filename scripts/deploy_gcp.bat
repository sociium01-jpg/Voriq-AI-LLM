@echo off
echo ===================================================
echo   Voriq AI Studio — GCP Cloud Run Deployment Script
echo   GCP Project: vaidyaq-prod-app-2026
echo   Region: asia-south1 (Mumbai)
echo ===================================================

set PROJECT_ID=vaidyaq-prod-app-2026
set REGION=asia-south1
set REPO_NAME=voriq-ai-repo
set REPO_URL=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%

echo [1/4] Ensuring Artifact Registry repository exists...
gcloud artifacts repositories create %REPO_NAME% --repository-format=docker --location=%REGION% --description="Voriq AI Container Repository" --project=%PROJECT_ID% || echo Repository already exists.

echo [2/4] Building and pushing API Gateway Image via GCP Cloud Build...
gcloud builds submit --tag %REPO_URL%/api-gateway:latest --dockerfile=infrastructure/docker/Dockerfile.api-gateway . --project=%PROJECT_ID%

echo [3/4] Deploying API Gateway service to GCP Cloud Run...
gcloud run deploy voriq-api-gateway --image=%REPO_URL%/api-gateway:latest --region=%REGION% --platform=managed --allow-unauthenticated --port=8000 --set-env-vars=ENVIRONMENT=production,LLM_PROVIDER=vllm --project=%PROJECT_ID%

echo [4/4] GCP Cloud Run Deployment Finished!
echo ===================================================
