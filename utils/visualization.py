import matplotlib.pyplot as plt
import io
import base64

def plot_feature_vs_yield(features, yields, xlabel):
    plt.figure()
    plt.scatter(features, yields, alpha=0.7)
    plt.xlabel(xlabel)
    plt.ylabel("Yield (tons/ha)")
    plt.title(f"{xlabel} vs Yield")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")
