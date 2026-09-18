def create_project_report(rows, columns, mean_house_value, top_category):
    return {
        "project": "DataAnalyzer",
        "rows": rows,
        "columns": columns,
        "mean_house_value": mean_house_value,
        "top_category_by_price": top_category,
    }


def get_conclusions():
    return [
        "Проект DataAnalyzer загружает реальные данные из CSV.",
        "Данные очищены от пропусков и готовы к анализу.",
        "NumPy используется для быстрой числовой статистики.",
        "Pandas используется для группировки и аналитических отчётов.",
        "Графики помогают объяснить результаты анализа.",
    ]