# WhatsApp Safety Bot - Step 1 Setup Instructions

## 🎯 Goal
Set up Flask webhook server to RECEIVE messages from WhatsApp (not send yet)

## 📋 Prerequisites
- Python 3.7+ installed
- Meta Developer account created
- WhatsApp test number from Meta

---

## 🚀 Step-by-Step Instructions

### 1️⃣ Install Flask
Open terminal/command prompt and run:
```bash
pip install Flask
```

### 2️⃣ Run the Flask Server
Navigate to the folder containing `app.py` and run:
```bash
python app.py
```

✅ You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**⚠️ KEEP THIS TERMINAL OPEN** - Don't close it!

---

### 3️⃣ Expose Server to Internet using ngrok

#### Install ngrok:
1. Go to: https://ngrok.com/download
2. Download for your OS (Windows/Mac/Linux)
3. Extract and install

#### Run ngrok:
Open a **NEW terminal** (keep Flask running in first one) and run:
```bash
ngrok http 5000
```

✅ You should see something like:
```
Forwarding    https://abcd-1234-5678.ngrok-free.app -> http://localhost:5000
```

**📝 COPY THIS URL** - You'll need it for Meta setup!

Example: `https://abcd-1234-5678.ngrok-free.app`

**⚠️ KEEP THIS TERMINAL OPEN TOO!**

---

### 4️⃣ Configure Webhook in Meta Developer

1. **Go to Meta Developer Console**
   - URL: https://developers.facebook.com/apps
   - Select your WhatsApp app

2. **Navigate to WhatsApp → Configuration**
   - Left sidebar: Click "WhatsApp" → "Configuration"

3. **Edit Webhook**
   - Click "Edit" button in Webhook section
   
4. **Enter Details:**
   - **Callback URL**: `https://YOUR-NGROK-URL.ngrok-free.app/webhook`
     - Example: `https://abcd-1234-5678.ngrok-free.app/webhook`
   - **Verify Token**: `mytoken123`
     - (Must match exactly what's in app.py)
   
5. **Click "Verify and Save"**
   - ✅ Should show "Valid callback URL"
   - ❌ If error, check:
     - Flask server is running?
     - ngrok is running?
     - URL copied correctly with `/webhook` at end?
     - Verify token is exactly `mytoken123`?

---

### 5️⃣ Subscribe to Messages

Still in Configuration page:

1. Find **Webhook fields** section
2. Click **"Manage"** button
3. Enable (✅ check) these fields:
   - ✅ **messages**
4. Click **"Save"**

---

### 6️⃣ Test It!

1. **Get Test Number**
   - In Meta Developer, go to: WhatsApp → API Setup
   - You'll see a test phone number provided by Meta
   - Add your personal WhatsApp number to "To" field

2. **Send Test Message**
   - Open WhatsApp on your phone
   - Send message to the Meta test number: `Hi`

3. **Check Terminal**
   - Look at the terminal where Flask is running
   - ✅ **Expected Output:**
     ```
     User said: Hi
     ```

---

## ✅ SUCCESS CRITERIA

You've completed Step 1 when:
1. Flask server is running (no errors)
2. ngrok is running and showing forwarding URL
3. Meta webhook verification succeeded
4. You send "Hi" from WhatsApp
5. Terminal shows: `User said: Hi`

---

## 🐛 Common Issues

### Issue 1: "Verification Failed" in Meta
- Check verify token is exactly `mytoken123` (case-sensitive)
- Make sure Flask is running
- Make sure ngrok URL ends with `/webhook`

### Issue 2: No output in terminal when sending WhatsApp message
- Check "messages" is subscribed in webhook fields
- Make sure you're sending to correct test number
- Check Flask terminal for any errors

### Issue 3: ngrok connection refused
- Make sure Flask is running on port 5000
- Try restarting ngrok

---

## 📝 When Done

Reply with:
- ✅ **"Step 1 done"** - if successful
- 🐛 **Screenshot/error message** - if stuck

Next: Step 2 will add bot responses! 🚀
