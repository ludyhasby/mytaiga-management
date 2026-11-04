import pandas as pd
from io import BytesIO

def readExcel(uploaded_file, sheetName:str, parseDates: list[str]) -> pd.DataFrame:
    uploaded_file.seek(0)
    df = pd.read_excel(uploaded_file, sheet_name=sheetName, parse_dates=parseDates)
    return df

def validateColumns(df: pd.DataFrame, label: str, expectedCol: list[str]) -> list[str]:
    missing = [col for col in expectedCol if col not in df.columns]
    if missing:
        return [f"{label}: kolom wajib tidak ditemukan: {', '.join(missing)}"]
    return []

def produceExcel(df: pd.DataFrame, sheet_name: str = "final_activities") -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl", datetime_format="yyyy-mm-dd hh:mm:ss") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name[:31])
    buffer.seek(0)
    return buffer.getvalue()