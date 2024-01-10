import pandas as pd
import re

URL_PATTERN = re.compile(
  r'^(?:http|ftp)s?://' # http:// or https://
  r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
  r'localhost|' # localhost...
  r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
  r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
  r'(?::\d+)?' # optional port
  r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_valid_url(url):
  return URL_PATTERN.match(url)

def is_valid_filename(filename):
  return str(filename).endswith('.png')

def validate_csv(file_path):
  errors = []
  try:
    df = pd.read_csv(file_path)
    if df.empty:
      errors.append("CSVファイルが空です")
    else:
      # CSVの列数をチェック（ファイル名とURLの2列が期待される）
      if len(df.columns) != 2:
        errors.append("CSVファイルの列数が不正です")
      else:
        for index, row in df.iterrows():
          if not is_valid_filename(row['ファイル名']):
            errors.append(f"{index + 1}行目: 拡張子をpngにしてください")
          if not is_valid_url(row['URL']):
            errors.append(f"{index + 1}行目: URLが正しい形式ではありません")
  except pd.errors.EmptyDataError:
    errors.append("CSVファイルが空です")
  except pd.errors.ParserError:
    errors.append("CSVファイルのフォーマットが不正です")
  except Exception as e:
    errors.append(f"読み込みエラーが発生しました: {e}")
  return errors
