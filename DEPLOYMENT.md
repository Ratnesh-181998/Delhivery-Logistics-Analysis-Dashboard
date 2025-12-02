# 🚀 Deployment Guide

Complete guide for deploying the Delhivery Logistics Analysis Dashboard to various platforms.

## 📋 Table of Contents

- [Streamlit Cloud](#streamlit-cloud-recommended)
- [Heroku](#heroku)
- [Docker](#docker)
- [AWS EC2](#aws-ec2)
- [Local Production](#local-production)

---

## 🌥️ Streamlit Cloud (Recommended)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Repository pushed to GitHub

### Step-by-Step Deployment

#### 1. Prepare Your Repository

Ensure these files are in your repository:
```
✅ app.py
✅ requirements.txt
✅ .streamlit/config.toml
✅ delhivery_data.csv (or your data file)
✅ README.md
```

#### 2. Push to GitHub

```bash
cd c:\Users\rattu\Downloads\Delhivery

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Delhivery Logistics Dashboard"

# Add remote
git remote add origin https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository: `Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard`
4. Set **Main file path**: `app.py`
5. Click **"Deploy"**

#### 4. Configuration

Streamlit Cloud will automatically:
- ✅ Install dependencies from `requirements.txt`
- ✅ Apply theme from `.streamlit/config.toml`
- ✅ Create a public URL: `https://your-app-name.streamlit.app`

#### 5. Update Your App

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main

# Streamlit Cloud will automatically redeploy
```

### Troubleshooting Streamlit Cloud

**Issue**: App won't start
- Check `requirements.txt` for correct versions
- Ensure `app.py` is in the root directory
- Check logs in Streamlit Cloud dashboard

**Issue**: Data file not found
- Ensure `delhivery_data.csv` is in the repository
- Check file path in `app.py`
- Verify file is not in `.gitignore`

---

## 🔷 Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

### Deployment Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create delhivery-logistics-dashboard

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🐳 Docker

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.log
.git
.gitignore
venv/
.venv/
*.md
```

### Build and Run

```bash
# Build image
docker build -t delhivery-dashboard .

# Run container
docker run -p 8501:8501 delhivery-dashboard

# Access at http://localhost:8501
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./delhivery_data.csv:/app/delhivery_data.csv
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

---

## ☁️ AWS EC2

### 1. Launch EC2 Instance

- **AMI**: Ubuntu 20.04 LTS
- **Instance Type**: t2.medium (recommended)
- **Security Group**: Allow port 8501

### 2. Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard.git
cd Delhivery-Logistics-Analysis-Dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### 3. Run as Service (systemd)

Create `/etc/systemd/system/delhivery-dashboard.service`:

```ini
[Unit]
Description=Delhivery Logistics Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Delhivery-Logistics-Analysis-Dashboard
Environment="PATH=/home/ubuntu/Delhivery-Logistics-Analysis-Dashboard/venv/bin"
ExecStart=/home/ubuntu/Delhivery-Logistics-Analysis-Dashboard/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable delhivery-dashboard
sudo systemctl start delhivery-dashboard
sudo systemctl status delhivery-dashboard
```

---

## 💻 Local Production

### Using Screen (Linux/Mac)

```bash
# Start screen session
screen -S delhivery-dashboard

# Run app
streamlit run app.py

# Detach: Ctrl+A, then D
# Reattach: screen -r delhivery-dashboard
```

### Using PM2 (Node.js process manager)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem.config.js
module.exports = {
  apps: [{
    name: 'delhivery-dashboard',
    script: 'streamlit',
    args: 'run app.py',
    interpreter: 'python3',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
  }]
}

# Start with PM2
pm2 start ecosystem.config.js

# Save configuration
pm2 save

# Setup startup script
pm2 startup
```

---

## 🔒 Security Best Practices

### 1. Environment Variables

Never commit sensitive data. Use `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml (add to .gitignore)
[database]
host = "your-db-host"
username = "your-username"
password = "your-password"
```

Access in code:
```python
import streamlit as st

db_host = st.secrets["database"]["host"]
```

### 2. HTTPS Setup

For production, use HTTPS:
- **Streamlit Cloud**: Automatic HTTPS
- **Custom Domain**: Use Nginx reverse proxy with Let's Encrypt

### 3. Authentication

Add basic authentication:
```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Your app code here
    st.write("Welcome to the dashboard!")
```

---

## 📊 Monitoring

### Application Logs

Logs are saved to `delhivery_app.log`. Monitor with:

```bash
# View logs in real-time
tail -f delhivery_app.log

# Search for errors
grep ERROR delhivery_app.log

# Count log levels
grep -c INFO delhivery_app.log
```

### Performance Monitoring

Add to your app:
```python
import time
import streamlit as st

@st.cache_data
def load_data():
    start_time = time.time()
    # Load data
    load_time = time.time() - start_time
    st.sidebar.metric("Data Load Time", f"{load_time:.2f}s")
```

---

## 🆘 Support

If you encounter issues:

1. Check [GitHub Issues](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/issues)
2. Review [Streamlit Documentation](https://docs.streamlit.io)
3. Contact: rattudacsit2021gate@gmail.com

---

**Happy Deploying! 🚀**
