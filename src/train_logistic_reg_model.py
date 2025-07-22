# Trains Logistic Regression Model ----------------------------------------------------------------------------
import pandas as pd  # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import joblib # type: ignore

from sklearn.model_selection import train_test_split # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore
from sklearn.utils.class_weight import compute_class_weight # type: ignore
from sklearn.metrics import accuracy_score, classification_report # type: ignore
from imblearn.over_sampling import SMOTE # type: ignore

# -- Loading the dataset
df = pd.read_csv('../data/student-mat.csv', sep=';')  

# -- Convert G3 (final grade) into categorical grades
# -- A: 18–20, B: 14–17, C: 10–13, D: 7–9, F: 0–6
bins = [-1, 6, 9, 13, 17, 20]
labels = ['F', 'D', 'C', 'B', 'A']
df['grade'] = pd.cut(df['G3'], bins=bins, labels=labels)

# -- Selecting relevant features for prediction
features = ['studytime', 'absences', 'failures', 'Medu', 'Fedu', 'G1', 'G2']
X = df[features].copy()
y = df['grade']

# -- Encoding non-numeric columns in X (if any)
non_numeric_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
label_encoders = {}
for col in non_numeric_cols:
    if set(X[col].unique()) == {'yes', 'no'}:
        X[col] = X[col].map({'yes': 1, 'no': 0})
    else:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

# -- Show grade distribution
print("Grade Distribution:\n", y.value_counts())

# -- Splitting into training and test sets (to preserve class balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -- Computing class weights for Logistic Regression
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weights_dict = dict(zip(np.unique(y_train), class_weights))
print("Class Weights:", class_weights_dict)

# -- Applying SMOTE to balance training data
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("Before SMOTE:\n", y_train.value_counts())
print("After SMOTE:\n", pd.Series(y_train_resampled).value_counts())

# -- Training the Logistic Regression model
model = LogisticRegression(
    multi_class='multinomial',
    solver='lbfgs',
    max_iter=1000,
    class_weight=class_weights_dict,
    random_state=42
)
model.fit(X_train_resampled, y_train_resampled)

# -- Making predictions on test data
y_pred = model.predict(X_test)

# -- Model Evaluation
print("\nAccuracy on test data:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -- Feature importance from logistic regression coefficients
coefficients = model.coef_
importance = np.mean(np.abs(coefficients), axis=0)  # Mean absolute importance across classes
feature_importance = sorted(zip(features, importance), key=lambda x: x[1], reverse=True)

print("\nFeature Importances (based on coefficients):")
for feature, importance_val in feature_importance:
    print(f"{feature}: {importance_val:.4f}")

# -- Saving model and encoders
joblib.dump(model, '../model/student_classifier.pkl')
print("\nLogistic Regression model saved to 'models/student_classifier.pkl'")

if label_encoders:
    joblib.dump(model, '../model/student_classifier.pkl')
    print("Label encoders saved to 'model/label_encoders.joblib'")