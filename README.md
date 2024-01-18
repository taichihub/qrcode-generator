# QRコード一括作成システム

CSVファイルのデータと任意の設定をもとにQRコードを一括で作成するシステムです

<br>

## 環境
- python (ver3.10)

<b>《使用ライブラリ》</b>

- pandas (ver2.1.4)
- qrcode (ver7.4.2)
- pillow (ver10.2.0)
- pytest (ver7.4.4)
- autopep8 (ver2.0.4)

※パッケージ管理にpipenvを使用<br>
・[pipenv(github)](https://github.com/pypa/pipenv)<br>
・[pipenv(qiita)](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a)

<br>

## 使用方法

<b>《環境構築》</b>

Pipfileで管理されているパッケージをインストール
```
pipenv install
```

<b>《前準備》</b>

- CSVデータの準備 (QRコード名, URL) <br>
※ dataフォルダの中に入れてください

[ フォーマットに即したCSVファイル例 ]
```
QRコード名,URL
A社.png,https://www.nintendo.co.jp/index.html
B社.png,https://www.sony.jp/
C社.png,https://www.capcom.co.jp/
D社.png,https://www.jp.square-enix.com/
E社.png,https://www.bandai.co.jp/
```

- 中央に表示するロゴ画像準備 (任意)<br>
※ 画像はpng形式でimgフォルダの中に入れてください<br>
※ imgフォルダの中に2枚以上画像を入れないでください

- QRコードの仕様決定 (src/setting.py)<br>
  - QRコードのバージョン (QR_VERSION)<br>
  - エラー訂正レベル (ERROR_CORRECTION_LEVEL)<br>
  - QRコードの大きさ (BOX_SIZE)<br>
  - 境界線のサイズ (BORDER_SIZE)<br>
  - QRコードの色 (QR_COLOR)<br>
  - QRコードの背景色 (QR_BACKGROUND_COLOR)<br>
  - 背景透過(任意) (QR_BACKGROUND_TRANSPARENT)<br>
  ※中央にロゴを挿入かつ背景透過のQRコードを作成する際はimgフォルダに入れる画像は背景透過済の画像を入れる必要があります。

<b>《実行》</b>

実行コマンド
```
python src/read_csv.py
```

実行後、qr_codeフォルダ内にCSVファイルごとにサブフォルダが生成され、その中にデータとsetting.pyで指定したQRコードの設定をもとに生成されたQRコードの画像ファイルが格納されます。

<br>

## ドキュメント
- [簡易モジュール構成図・シーケンス図](https://drive.google.com/file/d/1QVUi4KcGqufxJIqEsboudCzGMNTTiXNh/view?usp=sharing)