# ✅ Render Deployment Checklist

Before deploying to Render, ensure you have completed all these steps:

## 📋 Pre-Deployment Checklist

### 🔐 Security & Credentials
- [ ] ✅ **API Key Encrypted**: Ran `python encrypt_api_key.py` and got encrypted values
- [ ] ✅ **Master Key Secured**: Stored master key securely (password manager, etc.)
- [ ] ✅ **Admin Password Set**: Configured encrypted admin password
- [ ] ✅ **Sensitive Files Excluded**: `.gitignore` prevents committing secrets

### 📁 Repository Files
- [ ] ✅ **render.yaml**: Infrastructure as Code configuration file present
- [ ] ✅ **requirements.txt**: All dependencies listed with correct versions
- [ ] ✅ **Application Code**: FastAPI app in `app/` directory
- [ ] ✅ **Static Files**: Frontend files in `static/` directory
- [ ] ✅ **Documentation**: Deployment guides and README updated

### 🧪 Local Testing
- [ ] ✅ **Health Check**: `http://localhost:8000/api/v1/health` returns healthy
- [ ] ✅ **Main App**: `http://localhost:8000/` loads correctly
- [ ] ✅ **Admin Panel**: `http://localhost:8000/admin.html` shows login form
- [ ] ✅ **Authentication**: Can log in with password "secret"
- [ ] ✅ **Schema Validation**: Can validate schemas successfully
- [ ] ✅ **AI Integration**: OpenAI API responds correctly

## 🚀 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Create Render Service
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repository

### 3. Configure Environment Variables
Copy these exact values to Render dashboard:

```bash
SCHEMA_VALIDATOR_MASTER_KEY=1pfQUrO6gXjTc95uvcMI9tGyxAHP85JmTk-xQm08ons=
OPENAI_API_KEY=encrypted:Z0FBQUFBQm9RZzYzQTRRYlJ5WmxfMllpOEVCcERySE1KaFZmVWJsbExXTzVnMkpZbjRQd0p5dHQ2dHlrdWJLMXBzQXhsbmR2MUc3Tkk5anFzWU1GSnNKNG8yMEdhTlgxWXRRczdPZ3JtV2d4bVdWamtMR3Njd1hnQmVPREdkeWczRUFtdFNlMEZibjg2YzZDTGM4R1B5SXVudFA2YkhhWDl3anF4aDN3V3lCZk91RVhidDBfdTFQcWFnMnMwelRQdUNhcDlxN0J1c2JpbGFhR1BXdU1BdEl3b1JOZDd5RlIwbFlHeHJPX0tQaEg5cTEtOFF5bEQ1djdJNGhPSE1wc21VUTE3LUtrTVZscGJ1LThuemRGMUxWTDVEbkluTzRYc1pEVWp2ZWlMX2VSZjVIakxSbEtMUGRDekFVMzN5eVA5cHBuZG1TVGxPbFN4d19fUnU4elV3VFZqanlNUFo3VllaZloydUFybEhoUUFrX01HOGQ4VDdsZkdDUkl5YnZ0ZHZUcXM0NzBCeUptZzNBUHhKZUxwRFV6Q3dvVnVrZ3VjRHQzSFY0ZllFd3c3Uk5YdzRZek1FVHRPSmJ4cW1mRlprSUlBSmRrSmd2VEZaajJXWWU5RUUzZUxBM0JlV3ZneWRHWE14dVZlbXhyRzIwcDBjUEtuX2E1b1hVdjVHRnJGV1dvMGJDMUhQYU12LTI5V21kQzVpY3hlR0t3WHhXMGZESHN0d19iNHhlUXBjMjQwcjJYd05OeThXYTdpQnNickxEUTNNV285STAtRGNJenBWcUhQeVJWWUlweW9BXzJLNHdlRDZuTnhKRm9sdDFDazRkdllUSUEwNEpPa0wwU0kwNGN2djFFZW9fZQ==
ADMIN_PASSWORD=encrypted:Z0FBQUFBQm9RZzYzYURjMk9VdGdvam9MVFIwQVhrMmN1U2VOVlQxSFF0QURZc3dDeFZRcDgzb2dPUHYtX3BYNnB5NHJ4N3ZRaWJfUHFUdm1VLXBZWmxxX0lKUXp4Wl9ReHc9PQ==
DEBUG=false
AI_PROVIDER=openai
GPT_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
TOKENIZERS_PARALLELISM=false
```

### 4. Deploy & Test
- [ ] **Deploy**: Click "Create Web Service"
- [ ] **Monitor Logs**: Watch for successful startup
- [ ] **Test Health**: Visit `https://your-app.onrender.com/api/v1/health`
- [ ] **Test App**: Visit `https://your-app.onrender.com/`
- [ ] **Test Admin**: Visit `https://your-app.onrender.com/admin.html`

## 🎯 Post-Deployment Verification

### Functional Tests
- [ ] **Schema Validation Works**: Submit test schemas
- [ ] **AI Analysis Works**: Verify scores and recommendations
- [ ] **Admin Login Works**: Log in with "secret"
- [ ] **Admin Functions Work**: Test adding/editing best practices
- [ ] **Model Selection Works**: Change GPT model in admin panel

### Performance Tests
- [ ] **Response Times**: Check if responses are reasonable
- [ ] **Error Handling**: Test invalid inputs
- [ ] **Session Management**: Test admin session timeout

## 🔧 Troubleshooting Quick Reference

### If Build Fails:
1. Check Python version in logs
2. Verify all dependencies in `requirements.txt`
3. Check for typos in `render.yaml`

### If App Won't Start:
1. Verify environment variables are set correctly
2. Check master key matches encrypted values
3. Review startup logs for specific errors

### If AI Doesn't Work:
1. Confirm OpenAI API key is valid
2. Check encrypted API key format
3. Verify master key can decrypt the API key

### If Admin Login Fails:
1. Verify `ADMIN_PASSWORD` environment variable
2. Check admin password encryption format
3. Test locally first to isolate issue

## 📊 Expected Performance

### Free Tier Limitations:
- **Spin-up Time**: 30-60 seconds after inactivity
- **Memory**: 512MB RAM
- **CPU**: Shared CPU
- **Bandwidth**: 100GB/month
- **Build Time**: ~5-10 minutes

### Upgrade Recommendations:
- For production use: Consider Starter plan ($7/month)
- For high traffic: Professional plan with more resources

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Health check returns `{"status": "healthy"}`
- ✅ Main app loads without errors
- ✅ Admin panel shows login form
- ✅ Can log in and access admin functions
- ✅ Schema validation returns AI-powered scores
- ✅ All features work as expected locally

---

🚀 **Ready to Deploy!** Follow the steps above and your Schema Vibe Check will be live on the internet! 