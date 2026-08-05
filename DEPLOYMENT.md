# Voriq AI Studio — Production Deployment Guide

This guide provides step-by-step instructions to deploy **Voriq AI Studio** live on production infrastructure.

---

## 🏗 Deployment Architecture Options

| Component | VPS / Docker Compose (Fastest MVP) | Enterprise Managed Cloud (GCP / K8s) |
| :--- | :--- | :--- |
| **Web Studio UI** (`apps/web`) | Docker Container (Port 3000) | Vercel / GCP Cloud Run |
| **Admin Dashboard** (`apps/admin`) | Docker Container (Port 3001) | Vercel / GCP Cloud Run |
| **API Gateway** (`services/api-gateway`) | Docker Container (Port 8000) | GCP Cloud Run / GKE |
| **Database & Vector Store** | PostgreSQL 16 + `pgvector` container | GCP Cloud SQL (pgvector) |
| **Cache & Queue** | Redis container | GCP Memorystore for Redis |
| **Model Inference Engine** | Local vLLM / Ollama | Vertex AI Endpoints / GKE GPU Node Pool |
| **Training Engine** | Local GPU Worker / RunPod | Cloud-Agnostic Router (Vertex AI / GKE / On-Prem) |

---

## Option 1: Docker Compose Deployment (Single GPU Server / VPS)

### Step 1: Server Provisioning
Provision an Ubuntu 22.04 LTS GPU server (e.g. AWS g5.2xlarge, GCP Compute Engine with NVIDIA L4/A100, RunPod Pod, or Lambda Labs).

Install Docker & Docker Compose:
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
```

### Step 2: Clone Repository & Configure `.env`
```bash
git clone https://github.com/sociium01-jpg/Voriq-AI-LLM.git
cd Voriq-AI-LLM

cp .env.example .env
```

Edit `.env` for production:
```env
ENVIRONMENT=production
JWT_SECRET=generate_a_random_32_byte_secure_key_here
POSTGRES_PASSWORD=your_secure_db_password
POSTGRES_HOST=postgres
REDIS_HOST=redis

# Domain Settings
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Step 3: Launch Full Container Stack
```bash
docker-compose up -d --build
```

Verify all containers are running:
```bash
docker-compose ps
```

### Step 4: Configure Nginx & Let's Encrypt SSL

Install Nginx & Certbot:
```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

Configure `/etc/nginx/sites-available/vorik`:
```nginx
server {
    server_name app.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    server_name admin.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    server_name api.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site & obtain SSL certificates:
```bash
sudo ln -s /etc/nginx/sites-available/vorik /etc/nginx/sites-enabled/
sudo certbot --nginx -d app.yourdomain.com -d admin.yourdomain.com -d api.yourdomain.com
sudo systemctl reload nginx
```

---

## Option 2: Managed Cloud Deployment (Vercel + GCP / GKE)

### Step 1: Deploy Web Apps to Vercel
1. Import repository `sociium01-jpg/Voriq-AI-LLM` into Vercel.
2. For Web Studio:
   - Root Directory: `apps/web`
   - Framework Preset: Next.js
   - Environment Variable: `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`
3. For Admin Dashboard:
   - Root Directory: `apps/admin`
   - Framework Preset: Next.js

### Step 2: Deploy API Gateway to GCP Cloud Run or GKE
1. Build container image:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/vorik-api-gateway -f infrastructure/docker/Dockerfile.api-gateway .
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy vorik-api-gateway \
     --image gcr.io/YOUR_PROJECT_ID/vorik-api-gateway \
     --platform managed \
     --region asia-south1 \
     --allow-unauthenticated \
     --set-env-vars JWT_SECRET=your_secret,DATABASE_URL=postgresql+asyncpg://user:pass@cloudsql_ip:5432/vorik_ai
   ```

### Step 3: Connect Model Router & Cloud Providers
- Set Vertex AI Service Account keys or GKE workload identity.
- Configure `TrainingProviderRouter` in Admin Panel to switch dynamically between Vertex AI, GKE, and RunPod.
