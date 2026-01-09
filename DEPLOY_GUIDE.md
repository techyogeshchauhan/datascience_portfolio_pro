# 🚀 Deployment Guide

## Deploy to Render (FREE & Easy)

### Step 1: Create Render Account
1. Go to: https://render.com
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your repository: `techyogeshchauhan/datascience_portfolio_pro`
3. Configure:
   - **Name:** `soni-portfolio`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn send-email:app`
   - **Plan:** Free

### Step 3: Add Environment Variables
In Render dashboard, add:
- **Key:** `SENDER_PASSWORD`
- **Value:** Your Gmail App Password

### Step 4: Deploy
Click **"Create Web Service"**

Your site will be live at: `https://soni-portfolio.onrender.com`

---

## Deploy to Heroku

### Step 1: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Login
```bash
heroku login
```

### Step 3: Create App
```bash
heroku create soni-portfolio
```

### Step 4: Set Environment Variable
```bash
heroku config:set SENDER_PASSWORD=your_gmail_app_password
```

### Step 5: Deploy
```bash
git push heroku main
```

Your site will be live at: `https://soni-portfolio.herokuapp.com`

---

## Deploy to Vercel (Frontend Only)

For static frontend deployment:

```bash
npm install -g vercel
vercel
```

Note: You'll need to deploy Python backend separately.

---

## Environment Variables Needed

- `SENDER_PASSWORD` - Your Gmail App Password

---

## After Deployment

1. Get your deployment URL
2. Test the contact form
3. Check if emails are being sent
4. Update any hardcoded URLs if needed

---

**Recommended:** Use Render (easiest and free!)
