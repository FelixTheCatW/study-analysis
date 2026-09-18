import pandas as pd


def clean(dataframe: pd.DataFrame) -> pd.DataFrame:
    missing_before = dataframe.isna().sum().sum()

    df_clean = dataframe.copy()

    median_bedrooms = df_clean["total_bedrooms"].median()
    df_clean["total_bedrooms"] = df_clean["total_bedrooms"].fillna(median_bedrooms)

    df_clean = df_clean.drop_duplicates()

    missing_after = df_clean.isna().sum().sum()

    print("Пропусков до очистки:", missing_before)
    print("Пропусков после очистки:", missing_after)
    print("Размер после очистки:", df_clean.shape)

    return df_clean
