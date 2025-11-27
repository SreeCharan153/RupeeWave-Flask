# 🚀 **RupeeWave – Secure Banking ATM System (Flask + Supabase)**

A complete banking backend built with **Flask**, **Supabase**, and **JWT-based authentication**.
Designed for real-world banking workflows: account creation, PIN-based security, transactions, and audit logs.

---

# 🌐 **Live Deployment**

| Component              | URL                                                                              |
| ---------------------- | -------------------------------------------------------------------------------- |
| 🖥️ Frontend (Next.js) | [https://rupeewave.vercel.app](https://rupeewave.vercel.app)                     |
| ⚙️ Backend (Flask API) | [https://rupeewave-backend.onrender.com](https://rupeewave-backend.onrender.com) |

---

# 🧠 **Architecture Overview**

```
 ┌──────────────────────────┐
 │        Frontend          │
 │   Next.js + ShadCN UI    │
 │  Sends HttpOnly Cookies  │
 └──────────────┬───────────┘
                │
                ▼
 ┌──────────────────────────┐
 │        Backend           │
 │ Flask + JWT Auth System  │
 │  Access + Refresh Tokens │
 │  Role Based Permissions  │
 └──────────────┬───────────┘
                │
                ▼
 ┌──────────────────────────┐
 │        Supabase          │
 │ Postgres + Policies      │
 │ Secure RPC + Audits      │
 └──────────────────────────┘
```

---

# 🎯 **Key Features**

## 🔐 Authentication & Security

* JWT Access + Refresh workflow
* HttpOnly, Secure cookies
* Role-based access (Admin, Teller, Customer)
* Auto token refresh
* PIN verification + account lockout after 3 attempts
* Audit logging with IP + User-Agent
* Full middleware-based protection

## 🏦 Account Management

* Create new accounts
* Change PIN
* Update email/mobile
* Reset failed attempts

## 💸 Transactions

* Deposit
* Withdraw
* Transfer
* All actions logged
* Atomic DB operations

## 📜 History & Audits

* Transaction timeline
* Incoming/Outgoing transfers
* Teller/admin actions tracked

---

# 🔑 **Permission Matrix**

| Feature                 | Customer | Teller | Admin |
| ----------------------- | -------- | ------ | ----- |
| Create User             | ❌        | ❌      | ✅     |
| Create Account          | ❌        | ✅      | ✅     |
| Deposit/Withdraw        | ✅ (own)  | ✅      | ✅     |
| Transfer                | ✅        | ✅      | ✅     |
| Change PIN/Mobile/Email | ✅        | ✅      | ✅     |
| View History            | ❌        | ✅      | ✅     |
| View Audit Logs         | ❌        | ❌      | ✅     |

---

# 📂 **Backend Folder Structure (Flask Version)**

```
backend/
│── main.py
│── app/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── account_routes.py
│   │   ├── transaction_routes.py
│   │   ├── update_routes.py
│   │   └── history_routes.py
│   ├── services/
│   ├── schemas/
│   ├── core/
│   │   ├── security.py
│   │   └── middleware.py
│   └── config.py
│── requirements.txt
```

---

# 🛠 **Local Setup**

## 🔧 Backend (Flask)

```bash
pip install -r requirements.txt
python main.py
```

OR for production testing on Windows:

```bash
waitress-serve --port=8000 main:app
```

## 🎨 Frontend (Next.js)

```bash
npm install
npm run dev
```

---

# 🧪 **Testing (Pytest)**

```bash
pytest -v
```

Includes tests for:

* auth
* transactions
* PIN lockout
* account creation
* history validation

---

# 🔒 **Security Highlights**

* No JWT stored in browser storage
* All tokens are HttpOnly + Secure
* Refresh token rotation
* Account lockout logic
* Supabase RLS protecting all tables
* Server-side session verification
* Prevents replay attacks via expiration checks

---

# 📈 **Future Enhancements**

* Customer dashboard
* Teller analytics
* PDF statements
* SMS / Email alerts
* Search & filter history
* Fraud detection flags

---

# 🧑‍💻 **Author**

**Sri Charan Machabhakthuni**
Full-stack Developer | Python Backend Specialist

---

# ⭐ **Support & Credits**

If you like this project, consider starring the repo.
Your support motivates the next version of RupeeWave.
