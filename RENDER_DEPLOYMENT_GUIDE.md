# 🚀 Deploy Schema Vibe Check to Render

This guide will walk you through deploying your Schema Vibe Check application to Render.

## 📋 Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
3. **Encrypted Credentials**: You've already generated these with `encrypt_api_key.py`

## 🔐 Your Encrypted Credentials

**Master Key** (store securely):
```
SCHEMA_VALIDATOR_MASTER_KEY=1pfQUrO6gXjTc95uvcMI9tGyxAHP85JmTk-xQm08ons=
```

**Encrypted OpenAI API Key**:
```
OPENAI_API_KEY=encrypted:Z0FBQUFBQm9RZzYzQTRRYlJ5WmxfMllpOEVCcERySE1KaFZmVWJsbExXTzVnMkpZbjRQd0p5dHQ2dHlrdWJLMXBzQXhsbmR2MUc3Tkk5anFzWU1GSnNKNG8yMEdhTlgxWXRRczdPZ3JtV2d4bVdWamtMR3Njd1hnQmVPREdkeWczRUFtdFNlMEZibjg2YzZDTGM4R1B5SXVudFA2YkhhWDl3anF4aDN3V3lCZk91RVhidDBfdTFQcWFnMnMwelRQdUNhcDlxN0J1c2JpbGFhR1BXdU1BdEl3b1JOZDd5RlIwbFlHeHJPX0tQaEg5cTEtOFF5bEQ1djdJNGhPSE1wc21VUTE3LUtrTVZscGJ1LThuemRGMUxWTDVEbkluTzRYc1pEVWp2ZWlMX2VSZjVIakxSbEtMUGRDekFVMzN5eVA5cHBuZG1TVGxPbFN4d19fUnU4elV3VFZqanlNUFo3VllaZloydUFybEhoUUFrX01HOGQ4VDdsZkdDUkl5YnZ0ZHZUcXM0NzBCeUptZzNBUHhKZUxwRFV6Q3dvVnVrZ3VjRHQzSFY0ZllFd3c3Uk5YdzRZek1FVHRPSmJ4cW1mRlprSUlBSmRrSmd2VEZaajJXWWU5RUUzZUxBM0JlV3ZneWRHWE14dVZlbXhyRzIwcDBjUEtuX2E1b1hVdjVHRnJGV1dvMGJDMUhQYU12LTI5V21kQzVpY3hlR0t3WHhXMGZESHN0d19iNHhlUXBjMjQwcjJYd05OeThXYTdpQnNickxEUTNNV285STAtRGNJenBWcUhQeVJWWUlweW9BXzJLNHdlRDZuTnhKRm9sdDFDazRkdllUSUEwNEpPa0wwU0kwNGN2djFFZW9fZQ==
```

**Encrypted Admin Password**:
```
ADMIN_PASSWORD=encrypted:Z0FBQUFBQm9RZzYzYURjMk9VdGdvam9MVFIwQVhrMmN1U2VOVlQxSFF0QURZc3dDeFZRcDgzb2dPUHYtX3BYNnB5NHJ4N3ZRaWJfUHFUdm1VLXBZWmxxX0lKUXp4Wl9ReHc9PQ==
```

## 🌟 Deployment Methods

### Method 1: Infrastructure as Code (Recommended)

1. **Push the `render.yaml` file** to your repository root
2. **Connect your GitHub repo** to Render
3. **Set environment variables** in Render dashboard
4. **Deploy automatically**

### Method 2: Manual Setup via Dashboard

## 📝 Step-by-Step Instructions

### 1. Prepare Your Repository

Make sure your repository contains:
- ✅ `requirements.txt` with all dependencies
- ✅ `render.yaml` configuration file
- ✅ Your FastAPI application code
- ✅ `.gitignore` to exclude sensitive files

```bash
# Ensure you're not committing sensitive files
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Connect to Render

1. **Go to [render.com](https://render.com)** and sign in
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Select your schema_validator_service repo**

### 3. Configure Your Service

If using **Infrastructure as Code** (render.yaml):
- Render will detect the `render.yaml` file
- Most settings will be pre-configured

If doing **Manual Setup**:
- **Name**: `schema-vibe-check`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Set Environment Variables

⚠️ **CRITICAL**: Set these in the Render dashboard under "Environment":

```bash
# Master Key (REQUIRED - store securely!)
SCHEMA_VALIDATOR_MASTER_KEY=1pfQUrO6gXjTc95uvcMI9tGyxAHP85JmTk-xQm08ons=

# Encrypted API Key (REQUIRED)
OPENAI_API_KEY=encrypted:Z0FBQUFBQm9RZzYzQTRRYlJ5WmxfMllpOEVCcERySE1KaFZmVWJsbExXTzVnMkpZbjRQd0p5dHQ2dHlrdWJLMXBzQXhsbmR2MUc3Tkk5anFzWU1GSnNKNG8yMEdhTlgxWXRRczdPZ3JtV2d4bVdWamtMR3Njd1hnQmVPREdkeWczRUFtdFNlMEZibjg2YzZDTGM4R1B5SXVudFA2YkhhWDl3anF4aDN3V3lCZk91RVhidDBfdTFQcWFnMnMwelRQdUNhcDlxN0J1c2JpbGFhR1BXdU1BdEl3b1JOZDd5RlIwbFlHeHJPX0tQaEg5cTEtOFF5bEQ1djdJNGhPSE1wc21VUTE3LUtrTVZscGJ1LThuemRGMUxWTDVEbkluTzRYc1pEVWp2ZWlMX2VSZjVIakxSbEtMUGRDekFVMzN5eVA5cHBuZG1TVGxPbFN4d19fUnU4elV3VFZqanlNUFo3VllaZloydUFybEhoUUFrX01HOGQ4VDdsZkdDUkl5YnZ0ZHZUcXM0NzBCeUptZzNBUHhKZUxwRFV6Q3dvVnVrZ3VjRHQzSFY0ZllFd3c3Uk5YdzRZek1FVHRPSmJ4cW1mRlprSUlBSmRrSmd2VEZaajJXWWU5RUUzZUxBM0JlV3ZneWRHWE14dVZlbXhyRzIwcDBjUEtuX2E1b1hVdjVHRnJGV1dvMGJDMUhQYU12LTI5V21kQzVpY3hlR0t3WHhXMGZESHN0d19iNHhlUXBjMjQwcjJYd05OeThXYTdpQnNickxEUTNNV285STAtRGNJenBWcUhQeVJWWUlweW9BXzJLNHdlRDZuTnhKRm9sdDFDazRkdllUSUEwNEpPa0wwU0kwNGN2djFFZW9fZQ==

# Encrypted Admin Password (REQUIRED)
ADMIN_PASSWORD=encrypted:Z0FBQUFBQm9RZzYzYURjMk9VdGdvam9MVFIwQVhrMmN1U2VOVlQxSFF0QURZc3dDeFZRcDgzb2dPUHYtX3BYNnB5NHJ4N3ZRaWJfUHFUdm1VLXBZWmxxX0lKUXp4Wl9ReHc9PQ==

# Application Configuration
DEBUG=false
AI_PROVIDER=openai
GPT_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
TOKENIZERS_PARALLELISM=false
```

### 5. Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 5-10 minutes)
3. **Check logs** for any issues
4. **Test your application** at the provided URL

## 🧪 Testing Your Deployment

Once deployed, test these endpoints:

1. **Health Check**: `https://your-app.onrender.com/api/v1/health`
2. **Main App**: `https://your-app.onrender.com/`
3. **Admin Panel**: `https://your-app.onrender.com/admin.html`
   - Login with password: `secret`

## 🔧 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check Python version compatibility
   - Verify all dependencies in `requirements.txt`

2. **App Won't Start**:
   - Check environment variables are set correctly
   - Verify the master key matches the encrypted values

3. **AI Service Unavailable**:
   - Confirm OpenAI API key is valid and not expired
   - Check the encrypted API key format

4. **Admin Login Fails**:
   - Verify `ADMIN_PASSWORD` environment variable is set
   - Check if admin password encryption is working

### View Logs:
- Go to your service dashboard on Render
- Click "Logs" tab to see application output
- Look for any error messages

## 🎯 Next Steps

After successful deployment:

1. **Custom Domain** (optional): Add your own domain in Render settings
2. **SSL Certificate**: Automatically provided by Render
3. **Monitoring**: Set up health checks and alerts
4. **Scaling**: Upgrade from free tier if needed

## 🔒 Security Reminders

- ✅ Master key is encrypted and stored securely
- ✅ Admin panel is password protected
- ✅ API keys are encrypted in environment variables
- ✅ HTTPS is automatically enabled by Render
- ⚠️ Change the default admin password for production use

## 🆘 Support

If you encounter issues:

1. Check the [Render documentation](https://render.com/docs)
2. Review application logs in the Render dashboard
3. Verify all environment variables are correctly set
4. Test the application locally first to isolate issues

---

🎉 **Congratulations!** Your Schema Vibe Check application is now live and ready for the world to use! 