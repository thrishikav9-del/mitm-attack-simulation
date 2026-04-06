import os
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


# reproducibility
np.random.seed(42)
tf.random.set_seed(42)

os.makedirs("results/confusion_matrices", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)


# =========================
# BUILD LSTM MODEL
# =========================

def build_lstm(input_dim):

    model = Sequential()

    model.add(LSTM(64, input_shape=(input_dim,1)))

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

    print(f"\nTraining LSTM for {dataset} ({scaling})")

    # -----------------------
    # SAMPLE TRAIN DATA
    # -----------------------

    train_sample = 50000

    if trainX.shape[0] > train_sample:

        idx = np.random.choice(trainX.shape[0], train_sample, replace=False)

        trainX = trainX[idx]
        trainY = trainY.iloc[idx]


    # -----------------------
    # SAMPLE TEST DATA
    # -----------------------

    test_sample = 50000

    if testX.shape[0] > test_sample:

        idx = np.random.choice(testX.shape[0], test_sample, replace=False)

        testX = testX[idx]
        testY = testY.iloc[idx]


    # -----------------------
    # RESHAPE FOR LSTM
    # -----------------------

    trainX = trainX.reshape(trainX.shape[0], trainX.shape[1], 1)
    testX = testX.reshape(testX.shape[0], testX.shape[1], 1)


    # -----------------------
    # TRAIN MODEL
    # -----------------------

    model = build_lstm(trainX.shape[1])

    model.fit(
        trainX,
        trainY,
        epochs=5,
        batch_size=64,
        validation_split=0.1,
        verbose=1
    )


    # -----------------------
    # PREDICTIONS
    # -----------------------

    pred = model.predict(testX)

    pred = (pred > 0.5).astype(int).flatten()


    # -----------------------
    # METRICS
    # -----------------------

    acc = accuracy_score(testY, pred)
    prec = precision_score(testY, pred)
    rec = recall_score(testY, pred)
    f1 = f1_score(testY, pred)


    # -----------------------
    # CONFUSION MATRIX
    # -----------------------

    cm = confusion_matrix(testY, pred)

    plt.figure(figsize=(6,4))

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

    plt.title(f"LSTM Confusion Matrix - {dataset} ({scaling})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig(f"results/confusion_matrices/lstm_{dataset}_{scaling}.png")

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
results.append(["LSTM","ARP MITM","Standard",acc,prec,rec,f1])

acc,prec,rec,f1 = train_evaluate(*arp_mm,"ARP_MITM","MinMax")
results.append(["LSTM","ARP MITM","MinMax",acc,prec,rec,f1])


# =========================
# VIDEO INJECTION
# =========================

acc,prec,rec,f1 = train_evaluate(*video_std,"Video_Injection","Standard")
results.append(["LSTM","Video Injection","Standard",acc,prec,rec,f1])

acc,prec,rec,f1 = train_evaluate(*video_mm,"Video_Injection","MinMax")
results.append(["LSTM","Video Injection","MinMax",acc,prec,rec,f1])


# =========================
# ACTIVE WIRETAP
# =========================

acc,prec,rec,f1 = train_evaluate(*wire_std,"Active_Wiretap","Standard")
results.append(["LSTM","Active Wiretap","Standard",acc,prec,rec,f1])

acc,prec,rec,f1 = train_evaluate(*wire_mm,"Active_Wiretap","MinMax")
results.append(["LSTM","Active Wiretap","MinMax",acc,prec,rec,f1])


# =========================
# SAVE RESULTS TABLE
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

df.to_csv("results/tables/lstm_results.csv", index=False)

print("\nLSTM Results Table Generated\n")
print(df)