# 🏦 Credit Risk Scoring & Portfolio Analytics Simulator

An interactive credit risk underwriter simulator and portfolio analytics pipeline built using Python, Streamlit, and Chart.js. This application bridges the gap between data science exploration and business execution, allowing risk officers to evaluate individual applicant default probabilities dynamically while observing real-time impacts on overall validation cohort distributions.

---

## 🚀 System Features

- **Reactive Scoring Engine:** Generates credit scores ranging from 0 (High Risk) to 1000 (Low Risk) dynamically via multi-variable weight profiles.
- **Risk Component Decomposition:** Dual-layered analytics breaking down individual risk-factor and bonus-credit contributions.
- **Live Cohort Aggregation:** Simulates a 2,000-loan validation distribution tracker that responds instantly to active parameter updates.
- **Bespoke UI Layer:** Implements high-performance rendering by embedding hardware-accelerated Chart.js canvas modules natively inside the Streamlit state management thread.

---

## 🛠️ Technical Architecture & Stack

- **Model Exploration & Analysis:** Jupyter Notebook (`/notebooks/credit_risk_notebook.ipynb`) covering data preprocessing, feature distributions, and pipeline evaluation.
- **Backend Calculation Logic:** Python 3, NumPy Vectorization
- **Application Framework:** Streamlit State Management Suite
- **Visualization Engine:** Chart.js (v4.4.1), HTML5 Canvas, Vanilla JS
- **Interface Styling:** Minimalist semantic CSS component architecture with Tabler Icons integration

---

## 📊 Evaluation Baseline & Framework Performance

- **Core Model Classifier:** Logistic Regression (Configured with balanced class weights)
- **Primary Metric:** ROC-AUC Benchmark: `0.6400`
- **Validation Dataset Properties:** 10,000 credit records exhibiting a structural class imbalance (1.78% baseline default rate).

---

## 📈 Planned Engineering Optimizations

- Implement Synthetic Minority Over-sampling Techniques (**SMOTE**) via `imbalanced-learn` to better stabilize predictive performance bounds on highly skewed distributions.
- Integrate automated hyperparameter optimization pipelines utilizing the **Optuna** framework.
- Transition from local in-memory simulation states to real-time relational queries powered by an **AWS S3** data lake structure.
- Calibrate underwriting decision boundaries using specialized **Precision-Recall Tradeoff** curve optimization.
- Shift structural data splits to a **Walk-Forward Time-Series Cross-Validation** schema to prevent temporal data leakage.


