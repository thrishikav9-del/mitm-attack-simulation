import pandas as pd
import matplotlib.pyplot as plt


# ======================
# LOAD RESULT TABLES
# ======================

cnn = pd.read_csv("results/tables/table12_cnn_results.csv")
rnn = pd.read_csv("results/tables/table13_rnn_results.csv")
lstm = pd.read_csv("results/tables/lstm_results.csv")


metrics = ["Accuracy","Precision","Recall","F1 Score"]


# ======================
# FUNCTION TO DRAW GRAPH
# ======================

def plot_graph(df, model_name, save_name):

    plt.figure(figsize=(8,5))

    for i,row in df.iterrows():

        scores = [
            row["Accuracy"],
            row["Precision"],
            row["Recall"],
            row["F1 Score"]
        ]

        label = f'Dataset {i+1} {model_name} ({row["Feature Scaling Technique"]})'

        plt.plot(
            metrics,
            scores,
            marker='o',
            label=label
        )

    plt.title(f"Comparison of {model_name} Model Scores")
    plt.xlabel("Performance Evaluation Metrics")
    plt.ylabel("Scores")
    plt.legend()
    plt.grid(True)

    plt.savefig(f"results/{save_name}.png")

    plt.show()


# ======================
# CNN GRAPH
# ======================

plot_graph(cnn,"CNN","cnn_performance")


# ======================
# RNN GRAPH
# ======================

plot_graph(rnn,"RNN","rnn_performance")


# ======================
# LSTM GRAPH
# ======================

plot_graph(lstm,"LSTM","lstm_performance")