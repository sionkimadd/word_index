import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

class SentimentPlotter:

    def __init__(self, output_sentiment_csv):

        self.__output_sentiment_csv = output_sentiment_csv
        self.__sentiment_data = pd.read_csv(self.__output_sentiment_csv)
        self.__sentiment_data["datetime"] = pd.to_datetime(self.__sentiment_data["datetime"])
        self.__filtered_data = self.__sentiment_data[self.__sentiment_data["compound"] != 0]

    def plot_sentiment(self, search_word):

        plt.figure(figsize=(1.618 * 8, 8))
        plt.scatter(self.__filtered_data["datetime"], self.__filtered_data["compound"], c="k", alpha=0.3)

        daily_com_avg = self.__filtered_data.groupby(self.__filtered_data["datetime"].dt.date)["compound"].mean()
        plt.plot(daily_com_avg.index, daily_com_avg.values, "r-")

        plt.title(f"Index of {search_word}", fontsize=12)
        plt.ylabel("Score", fontsize=10)
        plt.ylim(-1, 1)
        plt.grid(True)
        plt.xticks(rotation=60, fontsize=7)
        
        png_dir = "static/png/"
        if not os.path.exists(png_dir):
            os.makedirs(png_dir)
    
        plot_filename = f"sentiment_plot_{search_word}.png"
        plot_filepath = os.path.join(png_dir, plot_filename)
        plt.savefig(plot_filepath)
        plt.close()

    @property
    def output_sentiment_csv(self):
        return self.__output_sentiment_csv
    
    @property
    def sentiment_data(self):
        return self.__sentiment_data
    
    @property
    def filtered_data(self):
        return self.__filtered_data