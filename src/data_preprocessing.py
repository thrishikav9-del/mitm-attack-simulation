import pandas as pd
import numpy as np
import os

print("Loading datasets...")

arp_data = pd.read_csv("data/ARP_MitM_dataset.csv")
arp_labels = pd.read_csv("data/ARP_MitM_labels.csv")

video_data = pd.read_csv("data/Video_Injection_dataset.csv")
video_labels = pd.read_csv("data/Video_Injection_labels.csv")

wire_data = pd.read_csv("data/Active_Wiretap_dataset.csv")
wire_labels = pd.read_csv("data/Active_Wiretap_labels.csv")

print("Merging datasets with labels...")

arp = pd.concat([arp_data, arp_labels], axis=1)
video = pd.concat([video_data, video_labels], axis=1)
wire = pd.concat([wire_data, wire_labels], axis=1)


def clean_data(df):

    print("Cleaning dataset...")

    df = df.drop_duplicates()
    df = df.dropna()

    df.replace([np.inf, -np.inf], 0, inplace=True)

    return df


arp = clean_data(arp)
video = clean_data(video)
wire = clean_data(wire)

print("Cleaned shapes:")
print("ARP:", arp.shape)
print("Video:", video.shape)
print("Wiretap:", wire.shape)

os.makedirs("processed_data", exist_ok=True)

arp.to_csv("processed_data/arp_clean.csv", index=False)
video.to_csv("processed_data/video_clean.csv", index=False)
wire.to_csv("processed_data/wire_clean.csv", index=False)

print("Data preprocessing completed successfully!")