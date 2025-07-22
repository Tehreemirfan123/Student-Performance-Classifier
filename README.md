![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)<br>
# 🎓 Student Performance Classifier

This project is a machine learning pipeline that predicts student performance levels based on various academic and background features. The final model classifies a student's final grade (`G3`) into letter grades: **A, B, C, D, or F**.

---

## 📂 Dataset

- Source: `student-mat.csv` from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Student+Performance)
- Contains attributes related to:
  - Student background (e.g., family education level, absences)
  - Academic performance (`G1`, `G2`, `G3`)
  - Personal and school-related factors

---

## 🧠 Goal

To build a machine learning model that:
- Categorizes students into **performance bands (A–F)**.
- Handles **class imbalance** using SMOTE and class weights.
- Uses **Logistic Regression** with hyperparameter tuning.
- Saves the final trained model for later deployment.
- Build an interactive user interface to get input from user and predict output (Using flutter for GUI).

---

## ⚙️ Features Used

| Feature     | Description                     |
|-------------|---------------------------------|
| `studytime` | Weekly study time               |
| `absences`  | Number of school absences       |
| `failures`  | Past class failures             |
| `Medu`      | Mother's education level        |
| `Fedu`      | Father's education level        |
| `G1`        | First-period grade              |
| `G2`        | Second-period grade             |

---

## 🧪 Model Training Process

1. **Preprocessing**
   - Convert `G3` into letter grades: A, B, C, D, F.
   - Encode any categorical values if present.
   - Stratified train-test split (80/20).
   
2. **Imbalance Handling**
   - Compute class weights.
   - Apply **SMOTE** to oversample minority classes in the training set.

3. **Model Training**
   - Use **Logistic Regression Model**.
   
4. **Evaluation**
   - Accuracy Score
   - Classification Report
   - Feature Importances

---

## 🧾 Outputs

- 📊 **Accuracy** and classification metrics on test set
- 🔍 **Confusion matrix** heatmap
- 📈 **Feature importance** ranking
- 💾 Trained model saved as: `student_classifier.pkl`

**Logistic Regression Model Training Result on Terminal**<br>
Accuracy on test data: 0.7088607594936709

Classification Report:
                    precision    recall  f1-score   support

              A       0.57      1.00      0.73         4
              B       0.71      0.62      0.67        16
              C       0.85      0.67      0.75        33
              D       0.54      0.93      0.68        14
              F       0.88      0.58      0.70        12

       accuracy                           0.71        79
      macro avg       0.71      0.76      0.70        79
      weighted avg    0.76      0.71      0.71        79
   
   Feature Importances (based on coefficients):
   G2: 2.3186
   Medu: 0.4434
   Fedu: 0.4087
   studytime: 0.3858
   failures: 0.3340
   G1: 0.3201
   absences: 0.0820

   Logistic Regression model saved to 'models/student_classifier.pkl'

---

**Project Running Method**
   - First run both the python files.
   - Run app.py code present in backend folder.
   - While its running, run flutter app, using *flutter run* command in vs code terminal.
   - Inspect and observe the model by entering different inputs.

## 👤  Author
**Name:**     Tehreem Irfan <br>
**Roll No:**  0090-BSCS-22  <br>
**Student:**  BSCS-A2

---

## 📦 Requirements

```bash
pip install pandas numpy scikit-learn matplotlib seaborn imbalanced-learn joblib
