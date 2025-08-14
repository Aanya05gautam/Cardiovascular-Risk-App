# 🫀 Cardiovascular Risk Prediction App

A **Machine Learning-based web application** that predicts the risk of cardiovascular disease using health and lifestyle information.
The goal is to help identify potential risks early and encourage preventive healthcare.

---

## 📌 Features

* **User-Friendly Form** – Input personal health details like age, gender, blood pressure, cholesterol, BMI, and habits.
* **Real-Time Prediction** – Instant cardiovascular risk assessment.
* **ML-Powered** – Uses trained models for accurate results.
* **Local Setup** – Can run directly on your computer without deployment.

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Flask (Python)
* **ML & Data Handling:** Pandas, NumPy, Scikit-learn
* **Model Storage:** Pickle (`.pkl`)

---

## 📂 Project Structure

```
├── app.py                  # Flask backend  
├── templates/              # HTML templates  
├── static/                 # CSS, JS, Images  
├── model.pkl               # Trained ML model  
├── requirements.txt        # Dependencies  
├── dataset.csv             # Training dataset  
└── README.md               # Documentation  
```

---

## 📊 Machine Learning Model

* **Algorithm Used:** Logistic Regression / Random Forest / XGBoost *(update with your actual choice)*
* **Workflow:**

  1. **Data Preprocessing:** Cleaning, encoding, and scaling data.
  2. **Model Training:** Using a cardiovascular dataset.
  3. **Evaluation:** Accuracy, precision, recall, F1-score.

---

## 🚀 Local Installation & Usage

**1. Clone the Repository**

```bash
git clone https://github.com/your-username/cardiovascular-risk-prediction.git
cd cardiovascular-risk-prediction
```

**2. Create Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the Application**

```bash
python app.py
```

**5. Open in Browser**
Go to `http://127.0.0.1:5000/` to use the app locally.

---

## 📷 Screenshots

<img width="954" height="537" alt="Screenshot 2025-08-14 185809" src="https://github.com/user-attachments/assets/c2af50d4-f649-426d-9e9d-c46b23b5033a" />
<img width="862" height="768" alt="Screenshot 2025-08-14 185816" src="https://github.com/user-attachments/assets/77783723-eda9-4114-b038-848be8c1844d" />

---

## 📌 Future Enhancements

* Deployment on Render / Heroku for online access.
* More advanced ML models for better accuracy.
* Graphical health insights for users.
* Mobile-friendly responsive design.

---

## 📜 License

Licensed under the MIT License – you’re free to use and modify this project.

