# ⚡ आसान इंस्टॉलेशन गाइड / Easy Installation Guide

## 🎯 तुरंत शुरू करें / Quick Start (3 Steps!)

### स्टेप 1: इंस्टॉल करें / Step 1: Install

```powershell
# PowerShell में यह कमांड चलाएं / Run this command in PowerShell:
.\install_windows.bat
```

**या / OR**

```powershell
# अगर ऊपर वाला काम न करे / If above doesn't work:

# Virtual environment बनाएं
python -m venv .venv

# Activate करें
.venv\Scripts\activate

# Packages इंस्टॉल करें (एक-एक करके)
python -m pip install --upgrade pip
python -m pip install Flask==3.0.0
python -m pip install Werkzeug==3.0.1
python -m pip install numpy==1.24.3
python -m pip install opencv-contrib-python==4.8.1.78
python -m pip install mysql-connector-python==8.2.0
python -m pip install Pillow==10.2.0
python -m pip install "qrcode[pil]==7.4.2"
python -m pip install python-dotenv==1.0.0
```

### स्टेप 2: Database बनाएं / Step 2: Create Database

```sql
-- MySQL में login करें
mysql -u root -p

-- Database बनाएं
CREATE DATABASE smart_attendance;

-- Exit
EXIT;
```

### स्टेप 3: Configuration करें / Step 3: Configure

```powershell
# .env file बनाएं
notepad .env
```

**इसमें ये लिखें / Write this:**

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Agrawal@@3170
DB_NAME=smart_attendance
```

**Save करें और बंद करें!**

## 🚀 चलाएं / Run

```powershell
# Virtual environment activate करें
.venv\Scripts\activate

# Application चलाएं
python app.py
```

**Browser में खोलें:** http://localhost:5000

**Login करें:**

- Username: `admin`
- Password: `admin123`

---

## ❌ अगर Error आए / If You Get Errors

### Error 1: "NumPy requires GCC"

```powershell
# यह version install करें
pip install numpy==1.24.3
```

### Error 2: "Module not found flask"

```powershell
# Virtual environment activate करें पहले
.venv\Scripts\activate

# फिर packages install करें
pip install Flask==3.0.0
```

### Error 3: "MySQL connection failed"

```powershell
# MySQL start करें
net start MySQL80

# .env file में password check करें
notepad .env
```

### Error 4: "Port 5000 in use"

```powershell
# दूसरा port use करें - app.py में last line बदलें:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 📝 पूरी Process Summary

1. ✅ Virtual environment बनाएं
2. ✅ Packages install करें (numpy==1.24.3 जरूर use करें)
3. ✅ MySQL में database बनाएं
4. ✅ .env file बनाएं अपने password के साथ
5. ✅ `python app.py` चलाएं
6. ✅ Browser में http://localhost:5000 खोलें
7. ✅ admin/admin123 से login करें

---

## 🆘 मदद चाहिए? / Need Help?

**पूरी जानकारी के लिए देखें / For complete details see:**

- `WINDOWS_SETUP.md` - Windows के लिए detailed guide
- `README.md` - Complete documentation
- `QUICKSTART.md` - 5-minute quick guide

---

## 💪 Done! अब सब काम करेगा! / Now Everything Will Work!

**अगर फिर भी problem हो:**

1. MySQL running है check करें: `net start MySQL80`
2. Virtual environment activate है check करें: `.venv\Scripts\activate`
3. .env में password सही है check करें: `notepad .env`

**Good Luck! 🎉**
