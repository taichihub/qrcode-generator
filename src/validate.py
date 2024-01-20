import pandas as pd
import re

# 列数
ROW_NUMBER = 2

# URLの正規表現
URL_PATTERN = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    # domain...
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
    r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def is_valid_url(url):
  # URLが有効な形式かどうかを検証する。
  # 正規表現を使用してURLの形式をチェックし、有効な形式であればTrueを返す。
  return URL_PATTERN.match(url)


def is_valid_filename(filename):
  # ファイル名が有効な形式（拡張子が'.png'であるか）を検証する。
  # ファイル名が'.png'で終わる場合にTrueを返す。
  return str(filename).endswith(".png")


# CSVファイルの構造を検証する
def validate_csv_structure(df):
  if df.empty:
    return ["CSVファイルが空です"]
  if len(df.columns) != ROW_NUMBER:
    return ["CSVファイルの列数が不正です"]
  return []


# 各行のデータを検証する
def validate_csv_row(df):
  errors = []
  for index, row in df.iterrows():
    if not is_valid_filename(row["ファイル名"]):
      errors.append(f"{index + 1}行目: 拡張子をpngにしてください")
    if not is_valid_url(row["URL"]):
      errors.append(f"{index + 1}行目: URLが正しい形式ではありません")
  return errors


# CSVファイル全体を検証する
def validate_csv(file_path):
  errors = []
  try:
    df = pd.read_csv(file_path)
    errors.extend(validate_csv_structure(df))
    errors.extend(validate_csv_row(df))
  except pd.errors.EmptyDataError:
    errors.append("CSVファイルが空です")
  except pd.errors.ParserError:
    errors.append("CSVファイルのフォーマットが不正です")
  except Exception as e:
    errors.append(f"読み込みエラーが発生しました: {e}")
  return errors
