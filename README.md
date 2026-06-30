# 🩺 Subscription Autopsy

> Track your subscriptions, measure how much value you *actually* get out of
> each one, and get roasted for the ones you've forgotten you're paying for.

**Subscription Autopsy** is a polished, dark-themed Flask web app that lets you
manually log your subscriptions (Netflix, Spotify, ChatGPT Plus, Adobe, Amazon
Prime, …) and find out how much money you're getting per use. It calculates a
**cost per use**, flags wasteful subscriptions, and generates a fresh, funny
**roast** for every one of them.

Built with **Python, Flask, SQLite, HTML5 and CSS3** — no JavaScript, no
frontend frameworks.

---

## ✨ Features

- **Dashboard** with summary cards for total monthly spending, estimated yearly
  spending, active subscriptions, potential money wasted, and average cost per
  use — plus your *worst* and *best value* subscriptions and a recent list.
- **Add / Edit / Delete** subscriptions with full **server-side validation**.
  Deletion shows a dedicated confirmation page (no JavaScript pop-ups).
- **Cost-per-use & waste analysis** with colour-coded **health badges**
  (Healthy / Warning / Waste) and a 0–100 **waste score** bar.
- **Roast generator** with 50+ unique lines split across the three health
  categories — a new roast is chosen on every page load.
- **Search** by name, **filter** by category / billing cycle / health, and
  **sort** by price, wastefulness, least used, or recently added — all using
  plain GET requests.
- **Statistics page**: most expensive, cheapest, highest/lowest cost per use,
  longest unused, averages, estimated yearly waste, and a pure-CSS health
  breakdown chart.
- **CSV export** of every subscription and its derived metrics.
- **Flash messages**, an attractive **empty state**, and a fully **responsive
  dark UI** with a gradient header, rounded cards, hover effects and smooth CSS
  animations.

---

## 🖼️ Screenshots

> _Placeholder — drop your own screenshots in here._

| Dashboard | Subscriptions | Statistics |
| --------- | ------------- | ---------- |
| _screenshot_ | _screenshot_ | _screenshot_ |

---

## 🚀 Quick Start (run it right now)

The easiest, fully cross-platform way to run the app — it creates a virtual
environment, installs the dependencies, and launches the server for you:

```bash
python run.py        # Windows
python3 run.py       # macOS / Linux
```

Or use the convenience scripts:

- **macOS / Linux:** `./run.sh`
- **Windows:** double-click `run.bat`

Then open <http://127.0.0.1:5000> (the launcher tries to open it automatically).

---

## 🛠️ Manual Setup

If you prefer to set things up yourself:

### 1. Clone the repository

```bash
git clone https://github.com/Nidaa26/SubSnitch.git
cd SubSnitch
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

The SQLite database (`database.db`) is created automatically on first run.
Visit <http://127.0.0.1:5000> in your browser.

---

## 📦 Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy

(All Python dependencies are pinned in `requirements.txt`.)

---

## 📂 Folder Structure

```
SubSnitch/
│
├── app.py                  # Application factory + entry point
├── config.py               # Configuration (secret key, database URI)
├── models.py               # SQLAlchemy model + derived-metric properties
├── routes.py               # All routes (Flask blueprint)
├── calculations.py         # Cost-per-use, health and waste-score logic
├── roast_generator.py      # 50+ roast messages by health category
├── utils.py                # Validation, filtering, sorting, CSV export
├── run.py                  # One-command cross-platform launcher
├── run.sh / run.bat        # Convenience launchers (macOS-Linux / Windows)
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html                 # Shared layout (header, nav, flash, footer)
│   ├── _subscription_card.html   # Reusable subscription card partial
│   ├── _subscription_form.html   # Reusable add/edit form partial
│   ├── dashboard.html
│   ├── subscriptions.html
│   ├── add_subscription.html
│   ├── edit_subscription.html
│   ├── delete_confirmation.html
│   └── statistics.html
│
└── static/
    └── css/
        └── style.css       # Dark SaaS theme (pure CSS)
```

---

## 🧮 How the analysis works

- **Cost per use** = price for the billing cycle ÷ number of uses this cycle.
- **Health** is classified as:
  - **Healthy** — cost per use below **$1**
  - **Warning** — cost per use between **$1 and $5**
  - **Waste** — cost per use above **$5**, *or* never used, *or* last used more
    than **45 days** ago.
- **Waste score (0–100)** blends how expensive each use is with how long the
  subscription has gone unused.

---

## 🔮 Future Improvements

- User accounts and authentication
- Email / push reminders before renewal dates
- Automatic bank or app-store import
- Charts and spending trends over time
- Currency selection and localisation
- Dark / light theme toggle

---

## 📄 License

Released under the [MIT License](https://opensource.org/licenses/MIT).
You're free to use, modify and share it.
