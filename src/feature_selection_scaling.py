import pandas as pd
import joblib

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

print("Loading cleaned datasets...")

arp = pd.read_csv("processed_data/arp_clean.csv")
video = pd.read_csv("processed_data/video_clean.csv")
wire = pd.read_csv("processed_data/wire_clean.csv")


# =============================
# FUNCTION TO PROCESS DATASET
# =============================

def process_dataset(df, name):

    print(f"\nProcessing {name} dataset")

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]


    # -------------------------
    # STANDARD SCALER
    # -------------------------

    print("Applying StandardScaler")

    std = StandardScaler()

    X_std = std.fit_transform(X)

    trainX, testX, trainY, testY = train_test_split(
        X_std,
        y,
        test_size=0.2,
        random_state=42
    )

    joblib.dump(
        (trainX, testX, trainY, testY),
        f"processed_data/{name}_std_split.pkl"
    )

    print(f"{name} StandardScaler split saved")


    # -------------------------
    # MINMAX SCALER
    # -------------------------

    print("Applying MinMaxScaler")

    mm = MinMaxScaler()

    X_mm = mm.fit_transform(X)

    trainX, testX, trainY, testY = train_test_split(
        X_mm,
        y,
        test_size=0.2,
        random_state=42
    )

    joblib.dump(
        (trainX, testX, trainY, testY),
        f"processed_data/{name}_mm_split.pkl"
    )

    print(f"{name} MinMaxScaler split saved")


# =============================
# RUN FOR ALL DATASETS
# =============================

process_dataset(arp, "arp")
process_dataset(video, "video")
process_dataset(wire, "wire")


print("\nFeature scaling and dataset splitting completed successfully!")