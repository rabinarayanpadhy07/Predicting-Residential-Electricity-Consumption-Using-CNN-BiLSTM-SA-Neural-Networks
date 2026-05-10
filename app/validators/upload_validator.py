from dataclasses import dataclass, field

import pandas as pd

from app.config import NUMERIC_COLUMNS, REQUIRED_COLUMNS


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


def validate_model_key(model_key, available_models):
    if model_key in available_models:
        return ValidationResult(True)
    return ValidationResult(
        False,
        [f"Unsupported model '{model_key}'. Choose one of: {', '.join(available_models)}."],
    )


def validate_dataframe(dataframe):
    errors = []
    if dataframe is None or dataframe.empty:
        return ValidationResult(False, ["The uploaded dataset is empty."])

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        errors.append("Missing required columns: " + ", ".join(missing_columns) + ".")
        return ValidationResult(False, errors)

    required = dataframe[REQUIRED_COLUMNS].replace("?", pd.NA)
    missing_counts = required.isna().sum()
    missing = [f"{column} ({count})" for column, count in missing_counts.items() if count > 0]
    if missing:
        errors.append("Missing or placeholder values found in: " + ", ".join(missing) + ".")

    dates = pd.to_datetime(dataframe["Date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    bad_dates = int(dates.isna().sum())
    if bad_dates:
        errors.append(f"Invalid Date values detected: {bad_dates}. Expected format is DD/MM/YYYY.")

    times = pd.to_datetime(dataframe["Time"], format="%H:%M:%S", errors="coerce")
    bad_times = int(times.isna().sum())
    if bad_times:
        errors.append(f"Invalid Time values detected: {bad_times}. Expected format is HH:MM:SS.")

    for column in NUMERIC_COLUMNS:
        numeric = pd.to_numeric(dataframe[column].replace("?", pd.NA), errors="coerce")
        bad_values = int(numeric.isna().sum())
        if bad_values:
            errors.append(f"Invalid numeric values in {column}: {bad_values}.")

    return ValidationResult(not errors, errors)
