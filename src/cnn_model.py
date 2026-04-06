import os
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# reproducibility
np.random.seed(42)
tf.random.set_seed(42)

os.makedirs("results/confusion_matrices", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)


# =========================
# CNN MODEL
# =========================

def build_cnn(input_dim):

    model = Sequential()

    model.add(Dense(128, activation="relu", input_shape=(input_dim,)))
    model.add(Dropout(0.3))

    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.3))

    model.add(Dense(32, activation="relu"))

    model.add(Dense(1, activation="sigmoid"))

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model


# =========================
# TRAIN + EVALUATE
# =========================

def train_evaluate(trainX, testX, trainY, testY, dataset, scaling):

    model = build_cnn(trainX.shape[1])

    model.fit(
        trainX,
        trainY,
        epochs=10,
        batch_size=32,
        validation_split=0.1
    )

    pred = model.predict(testX)
    pred = (pred > 0.5).astype(int).flatten()

    acc = accuracy_score(testY, pred)
    prec = precision_score(testY, pred)
    rec = recall_score(testY, pred)
    f1 = f1_score(testY, pred)

    cm = confusion_matrix(testY, pred)

    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

    plt.title(f"CNN Confusion Matrix - {dataset} ({scaling})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig(f"results/confusion_matrices/cnn_{dataset}_{scaling}.png")
    plt.close()

    return acc, prec, rec, f1


# =========================
# LOAD DATA
# =========================

print("Loading dataset splits...")

arp_std = joblib.load("processed_data/arp_std_split.pkl")
arp_mm = joblib.load("processed_data/arp_mm_split.pkl")

video_std = joblib.load("processed_data/video_std_split.pkl")
video_mm = joblib.load("processed_data/video_mm_split.pkl")

wire_std = joblib.load("processed_data/wire_std_split.pkl")
wire_mm = joblib.load("processed_data/wire_mm_split.pkl")


results = []


# =========================
# ARP MITM
# =========================

acc,prec,rec,f1 = train_evaluate(*arp_std,"ARP_MITM","Standard")
results.append(["CNN","ARP MITM","Standard",acc,prec,rec,f1])

acc,prec,rec,f1 = train_evaluate(*arp_mm,"ARP_MITM","MinMax")
results.append(["CNN","ARP MITM","MinMax",acc,prec,rec,f1])


# =========================
# VIDEO INJECTION
# =========================

acc,prec,rec,f1 = train_evaluate(*video_std,"Video_Injection","Standard")
results.append(["CNN","Video Injection","Standard",acc,prec,rec,f1])

acc,prec,rec,f1 = train_evaluate(*video_mm,"Video_Injection","MinMax")
results.append(["CNN","Video Injection","MinMax",acc,prec,rec,f1])


# =========================
# ACTIVE WIRETAP
# =========================

acc,prec,rec,f1 = train_evaluate(*wire_std,"Active_Wiretap","Standard")
results.append(["CNN","Active Wiretap","Standard",acc,prec,rec,f1])

acc,prec,rec,f1 = train_evaluate(*wire_mm,"Active_Wiretap","MinMax")
results.append(["CNN","Active Wiretap","MinMax",acc,prec,rec,f1])


# =========================
# TABLE 12
# =========================

df = pd.DataFrame(
    results,
    columns=[
        "Model Used",
        "Data Set Used",
        "Feature Scaling Technique",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]
)

df.to_csv("results/tables/table12_cnn_results.csv", index=False)

print("\nTable 12 generated successfully\n")
print(df)