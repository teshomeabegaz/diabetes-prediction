import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diabetes Probability Calculator", page_icon="🩺", layout="centered")

# Coefficients read from the supplied formula.csv.
COEF = {
    "const": -6.099303,
    "age": 0.031035,
    "systolic_bp": -0.004444,
    "glucose": 0.021960,
    "hypertension": 0.497003,
    "sex_Male": -0.133375,
    "smoking_Yes": 1.077169,
}

st.title("Diabetes Probability Calculator")
st.caption("MU-CHS Faculty of Public Health · Health Informatics Department")

st.warning(
    "Educational/research prototype only. This calculator uses coefficients from a supplied "
    "regression-results CSV; it has not been independently validated and must not be used "
    "to diagnose diabetes or make clinical decisions."
)

st.subheader("Enter predictor values")
with st.form("diabetes_prediction"):
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=45, step=1)
    systolic_bp = st.number_input("Systolic blood pressure (mmHg)", min_value=50.0, max_value=300.0, value=120.0, step=1.0)
    glucose = st.number_input(
        "Glucose",
        min_value=0.0,
        max_value=2000.0,
        value=100.0,
        step=1.0,
        help="Enter glucose using the same unit and measurement definition as the model's training data."
    )
    hypertension = st.selectbox("Hypertension (original coding assumed: 1 = Yes, 0 = No)", ["No", "Yes"])
    sex = st.selectbox("Sex", ["Female", "Male"])
    smoking = st.selectbox("Smoking (original coding assumed: 1 = Yes, 0 = No)", ["No", "Yes"])
    submitted = st.form_submit_button("Estimate probability", type="primary")

if submitted:
    htn = 1 if hypertension == "Yes" else 0
    male = 1 if sex == "Male" else 0
    smoker = 1 if smoking == "Yes" else 0

    eta = (
        COEF["const"]
        + COEF["age"] * age
        + COEF["systolic_bp"] * systolic_bp
        + COEF["glucose"] * glucose
        + COEF["hypertension"] * htn
        + COEF["sex_Male"] * male
        + COEF["smoking_Yes"] * smoker
    )
    # Numerically stable logistic function
    if eta >= 0:
        probability = 1 / (1 + math.exp(-eta))
    else:
        exp_eta = math.exp(eta)
        probability = exp_eta / (1 + exp_eta)

    st.subheader("Model estimate")
    st.metric("Estimated probability of diabetes", f"{probability:.1%}")
    st.write(f"Linear predictor (η): `{eta:.4f}`")
    st.progress(float(min(max(probability, 0.0), 1.0)))

    result = pd.DataFrame([{
        "age_years": age,
        "systolic_bp_mmhg": systolic_bp,
        "glucose_entered": glucose,
        "hypertension": hypertension,
        "sex": sex,
        "smoking": smoking,
        "linear_predictor_eta": eta,
        "estimated_probability": probability,
        "estimated_probability_percent": probability * 100,
    }])
    st.download_button(
        "Download prediction as CSV",
        data=result.to_csv(index=False).encode("utf-8"),
        file_name="diabetes_prediction.csv",
        mime="text/csv",
    )

with st.expander("Model coefficients and odds ratios"):
    coef_table = pd.DataFrame([
        ["Intercept", -6.099303, 0.002244, 0.009825],
        ["Age", 0.031035, 1.031521, 0.012860],
        ["Systolic BP", -0.004444, 0.995566, 0.808960],
        ["Glucose", 0.021960, 1.022203, 0.033055],
        ["Hypertension", 0.497003, 1.643788, 0.342171],
        ["Male sex", -0.133375, 0.875137, 0.672503],
        ["Smoking: Yes", 1.077169, 2.936355, 0.000758],
    ], columns=["Term", "Coefficient", "Odds ratio", "p-value"])
    st.dataframe(coef_table, use_container_width=True, hide_index=True)

st.subheader("Before using this model")
st.markdown(
    "- Confirm the original coding of hypertension, sex, and smoking.\n"
    "- Confirm the glucose unit and how glucose was measured in the training data.\n"
    "- Validate discrimination and calibration on independent data before considering any clinical use.\n"
    "- Do not interpret the probability as a diagnosis or as a validated clinical risk score."
)
