import pandas as pd
import re

def validate_csv(file_path):
  # URLの正規表現パターン
  url_pattern = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

  errors = [] # バリデーションエラーを格納するリスト
  
  try:
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
      if not str(row['ファイル名']).endswith('.png'):
        errors.append(f"{index + 1}行目: 拡張子をpngにしてください")
      if not url_pattern.match(str(row['URL'])):
        errors.append(f"{index + 1}行目: URLが正しい形式ではありません")
  except Exception as e:
    errors.append(f"バリデーションエラーが発生しました: {e}")
  return errors
