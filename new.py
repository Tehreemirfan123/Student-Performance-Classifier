import tkinter as tk
from tkinter import messagebox
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import joblib  # type: ignore

# Load the trained model
model = joblib.load('model/student_classifier.pkl')

# Define feature names used in training
feature_names = [
    'age',
    'study_time',
    'higher_education',
    'absences',
    'previous_grade',
    'extracurricular',
    'internet_usage',
    'family_support',
]

class StudentPerformanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Performance Predictor")
        self.geometry("450x550")
        self.configure(bg="#f0f0f0")

        self.inputs = {}

        # Create input fields with hints for specific features
        hints = {
            'age': "(from 15 to 22)",
            'study_time': "(1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)",
            'higher_education': " (yes or no)",
            'absences': "(0-93)",
            'previous_grade': "(0-20)",
            'extracurricular': "(yes or no)",
            'internet_usage': "(yes or no)",
            'family_support': "(yes or no)",
        }

        for idx, feature in enumerate(feature_names):
            # Label with hint
            label_text = feature.replace("_", " ").title()
            if feature in hints:
                label_text += f" {hints[feature]}"
            label = tk.Label(self, text=label_text, bg="#f0f0f0", font=("Arial", 12))
            label.pack(pady=(10 if idx == 0 else 5, 2))

            entry = tk.Entry(self, width=30, font=("Arial", 12))
            entry.pack()
            self.inputs[feature] = entry

        # Predict button
        predict_button = tk.Button(self, text="Predict", command=self.update_prediction,
                                   font=("Arial", 12), bg="#4CAF50", fg="white")
        predict_button.pack(pady=20)

        # Result label
        self.result_label = tk.Label(self, text="", bg="#f0f0f0", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)

    def update_prediction(self):
        try:
            # Get input values
            input_values = []
            for feature in feature_names:
                value = self.inputs[feature].get()
                if value.strip() == "":
                    raise ValueError(f"Please enter a value for '{feature.replace('_', ' ').title()}'")
                # Convert absences to int, others to float
                if feature == "absences":
                    input_values.append(int(value))
                else:
                    input_values.append(float(value))

            # Prepare DataFrame input
            input_df = pd.DataFrame([input_values], columns=feature_names)

            # Get prediction
            pred_probs = model.predict_proba(input_df)[0]
            predicted_class = model.predict(input_df)[0]
            confidence = round(pred_probs[predicted_class] * 100, 2)

            self.result_label.config(
                text=f"Predicted Class: {predicted_class} (Confidence: {confidence}%)",
                fg="#333"
            )

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")


if __name__ == "__main__":
    app = StudentPerformanceApp()
    app.mainloop()
