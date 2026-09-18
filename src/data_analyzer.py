import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def describe_columns_ru(column_descriptions):
    for column, description in column_descriptions.items():
        print(column, "—", description)


def basic_info(dataframe):
    print("Размер таблицы:", dataframe.shape)
    print("Колонки:", dataframe.columns.tolist())
    print()
    dataframe.info()


class DataAnalyzer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_numeric_statistics(self, column):
        values = self.dataframe[column].to_numpy()
        return {
            "min": np.min(values),
            "max": np.max(values),
            "mean": np.mean(values),
            "std": np.std(values),
        }

    def get_group_report(self, group_column, value_column):
        report = (
            self.dataframe.groupby(group_column)[value_column]
            .agg(["count", "mean", "min", "max"])
            .sort_values(by="mean", ascending=False)
        )
        return report


def _save_figure(fig, filename, save_dir):
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    filepath = save_dir / filename
    fig.savefig(filepath, bbox_inches="tight")
    plt.close(fig)
    print("График сохранён:", filepath)


def plot_histogram(dataframe, column, save_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(dataframe[column], bins=30)
    ax.set_title("Распределение стоимости жилья")
    ax.set_xlabel("Стоимость жилья")
    ax.set_ylabel("Количество районов")
    ax.grid(True)
    _save_figure(fig, "house_value_histogram.png", save_dir)


def plot_scatter(dataframe, x_column, y_column, save_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(dataframe[x_column], dataframe[y_column], alpha=0.25)
    ax.set_title("Зависимость стоимости жилья от дохода")
    ax.set_xlabel("Медианный доход")
    ax.set_ylabel("Стоимость жилья")
    ax.grid(True)
    _save_figure(fig, "income_vs_value_scatter.png", save_dir)


def plot_group_report(group_report, save_dir):
    fig, ax = plt.subplots(figsize=(8, 5))
    group_report["mean"].plot(kind="bar", ax=ax)
    ax.set_title("Средняя стоимость жилья по близости к океану")
    ax.set_xlabel("Близость к океану")
    ax.set_ylabel("Средняя стоимость")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True)
    _save_figure(fig, "group_report_bar.png", save_dir)