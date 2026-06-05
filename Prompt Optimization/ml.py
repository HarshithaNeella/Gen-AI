#for data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

#preprocessing
from sklearn.model_selection import train_test_split, RandomizedSearchCV 
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

df = pd.read_csv(r"D:\DS_GENAI_Task_1\AQI.csv")

print("\nDataset Info:\n")
print(df.info())

print("First 5 Rows:\n")
print(df.head())

print("\nMissing Values:\n")
print(df.isnull().sum())

print("\nStatistical Summary:\n")
print(df.describe())


# Remove duplicate rows
df = df.drop_duplicates()

# remove target nulls
df = df.dropna(subset=["AQI"])

# remove unwanted columns
remove_cols = []

for col in df.columns:
    
    col_lower = col.lower()

    if "id" in col_lower:
        remove_cols.append(col)

    if "date" in col_lower:
        remove_cols.append(col)

    if "unnamed" in col_lower:
        remove_cols.append(col)

df = df.drop(columns=remove_cols, errors="ignore")


print("\n================ EDA ================\n")

# AQI Distribution
plt.figure(figsize=(8,5))
sns.histplot(df["AQI"], kde=True)
plt.title("AQI Distribution")
plt.show()

# Correlation Heatmap
numeric_df = df.select_dtypes(include=np.number)

plt.figure(figsize=(14,10))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.show()

# features and target
X = df.drop(["AQI"], axis=1)
y = df["AQI"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# numerical columns
num_cols = X.select_dtypes(include=np.number).columns.tolist()

# categorical columns
cat_cols = X.select_dtypes(exclude=np.number).columns.tolist()

# preprocessing
transform = ColumnTransformer(
    transformers=[
        ("scaler", StandardScaler(), num_cols),
        ("encoder", OrdinalEncoder(), cat_cols)
    ],
    remainder="passthrough"
)

# pipeline
pipe = Pipeline(
    steps=[
        ("transform", transform),
        ("model", RandomForestRegressor(random_state=42))
    ]
)

# hyperparameters
param_dist = {

    "model__n_estimators": [50, 100, 150],

    "model__max_depth": [5, 10, 15, None],

    "model__min_samples_split": [2, 5, 10],

    "model__min_samples_leaf": [1, 2, 4]
}

# random search
start_time = time.time()

random_search = RandomizedSearchCV(
    pipe,
    param_distributions=param_dist,
    cv=5,
    random_state=42,
    n_iter=10,
    scoring="r2",
    n_jobs=-1
)
random_search.fit(X_train, y_train)

training_time = time.time() - start_time

print("\nBest Parameters:\n")
print(random_search.best_params_)

print("\nBest CV Score:\n")
print(random_search.best_score_)

# predictions
y_pred = random_search.predict(X_test)

# test score
test_r2 = r2_score(y_test, y_pred)

print("\nTesting R2 Score:\n")
print(test_r2)

print("\nTraining Time:\n")
print(training_time)

# results dataframe
results_df = pd.DataFrame(
    random_search.cv_results_
)

# useful columns
results_df = results_df[
    [
        "params",
        "mean_test_score",
        "std_test_score",
        "rank_test_score"
    ]
]

# add extra metrics
results_df["test_r2"] = test_r2
results_df["training_time"] = training_time

print(results_df.head())

# save csv
results_df.to_csv("AQI_Model_Results.csv", index=False)

print("\nCSV Saved Successfully!")
