import sys
import pandas as pd
import numpy as np
import matplotlib
from pathlib import Path

matplotlib.use("Agg")

from src.data_loader import load_dataset
from src.data_clean import clean
from src.statistics_utils import calculate_numpy_statistics
from src.data_analyzer import (
    describe_columns_ru,
    basic_info,
    plot_histogram,
    plot_scatter,
    plot_group_report,
    DataAnalyzer,
)
from src.report_utils import create_project_report, get_conclusions

PROJECT_DIR = Path(__file__).resolve().parent.parent
PLOT_DIR = PROJECT_DIR / "plots"

URL = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv"

TARGET_COL = "median_house_value"

COLUMN_DESCRIPTIONS = {
    "longitude": "долгота района",
    "latitude": "широта района",
    "housing_median_age": "медианный возраст домов",
    "total_rooms": "общее количество комнат",
    "total_bedrooms": "общее количество спален",
    "population": "население района",
    "households": "количество домохозяйств",
    "median_income": "медианный доход",
    TARGET_COL: "медианная стоимость жилья",
    "ocean_proximity": "близость к океану",
}


def main():
    print("Библиотеки подключены")
    print("Pandas:", pd.__version__)
    print("NumPy:", np.__version__)

    assert pd is not None
    assert np is not None

    df = load_dataset(URL)
    assert len(df) > 0
    assert TARGET_COL in df.columns

    print()
    print("Первые строки датасета:")
    print(df.head().to_string())

    print()
    describe_columns_ru(COLUMN_DESCRIPTIONS)

    print()
    basic_info(df)

    assert TARGET_COL in df.columns
    assert "ocean_proximity" in df.columns

    df_clean = clean(df)
    assert df_clean.isna().sum().sum() == 0
    assert len(df_clean) > 0

    numpy_stats = calculate_numpy_statistics(df_clean[TARGET_COL].to_numpy())

    print()
    print("NumPy-статистика median_house_value:")
    for key, value in numpy_stats.items():
        print(key, ":", value)

    assert numpy_stats["max"] >= numpy_stats["min"]
    assert numpy_stats["mean"] > 0

    print()
    print("Pandas-описательная статистика:")
    print(df_clean.describe().to_string())

    analyzer = DataAnalyzer(df_clean)
    group_report = analyzer.get_group_report("ocean_proximity", TARGET_COL)

    print()
    print("Средняя стоимость жилья по близости к океану:")
    print(group_report.to_string())

    assert "mean" in group_report.columns
    assert group_report.shape[0] > 0

    print()
    print("Визуализация:")
    plot_histogram(df_clean, TARGET_COL, PLOT_DIR)
    plot_scatter(df_clean, "median_income", TARGET_COL, PLOT_DIR)
    plot_group_report(group_report, PLOT_DIR)

    assert len(group_report) > 0

    print()
    print("Статистика через класс DataAnalyzer:")
    print(analyzer.get_numeric_statistics(TARGET_COL))
    print(analyzer.get_group_report("ocean_proximity", TARGET_COL).to_string())

    top_category = group_report["mean"].idxmax()

    project_report = create_project_report(
        rows=len(df_clean),
        columns=df_clean.shape[1],
        mean_house_value=float(df_clean[TARGET_COL].mean()),
        top_category=top_category,
    )

    print()
    print("Итоговый отчёт проекта:")
    for key, value in project_report.items():
        print(key, ":", value)

    conclusions = get_conclusions()

    print()
    print("Выводы:")
    for item in conclusions:
        print("-", item)

    assert project_report["rows"] > 1000
    assert len(conclusions) == 5


if __name__ == "__main__":
    main()