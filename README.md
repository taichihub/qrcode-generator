## ステータス
執筆中

# QRコード一括作成システム

CSVファイルのデータと任意の設定をもとにQRコードを一括で作成するシステムです

## 環境
- python (ver3.10.2)

<b>《使用ライブラリ》</b>
- pandas (ver2.1.4)
- qrcode (ver7.4.2)
- pillow (ver10.2.0)
- pytest (ver7.4.4)
- autopep8 (ver2.0.4)

※パッケージ管理にpipenvを使用<br>
・[pipenv(github)](https://github.com/pypa/pipenv)<br>
・[pipenv(qiita)](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a)

## 使用方法
### 環境構築
- 自分のローカル環境にクローンする
```
git clone git@github.com:frame-and-surface/app_qrcode-generator_main.git
```
- クローンしたディレクトリに移動
```
cd app_qrcode-generator_main
```
- Pipfileで管理されているパッケージをインストール
```
pipenv install
```
`✔ Success!`の文字が表示されればインストール成功
- 仮想環境に入る
```
pipenv shell
```

### 事前準備：ディレクトリ構造の理解
```
app_qrcode-generator_main/
├── .github/ (編集厳禁)
├── config/
│   ├── log_messages.yml (編集厳禁)
│   ├── setting.py (QRコード生成時の設定ファイル)(※1)
│   └── setup_log.py (編集厳禁)
├── data/ (CSVファイルを配置するフォルダ)(※2)
├── img/ (QRコードの中央に画像を挿入する際に使用するフォルダ)(※3)
├── qr_code/ (生成されたQRコードガ格納されるディレクトリ)(※4)
├── src/ (編集厳禁)
├── test/ (編集厳禁)
├── .gitignore (編集厳禁)
├── Dockerfile (編集厳禁)
├── Makefile (編集厳禁)
├── Pipfile (編集厳禁)
├── Pipfile.lock (編集厳禁)
├── pytest.ini (編集厳禁)
├── README.md (編集厳禁)
└── setup.py (編集厳禁)
```
(※1)QRコードを生成する際の設定を詳しい設定方法は後述の「`setting.py`の使用方法(QRコード生成に関する設定)」を参考にしてください<br>
(※2)dataフォルダ配下にCSVファイルを配置します。詳しい仕様は後述の「dataフォルダに関するルール」「CSVファイル例」を参考にしてください。<br>
(※3)imgフォルダ配下にQRコード中央に配置する画像を配置します。詳しい仕様は後述の「imgフォルダに関するルール」を参考にしてください。<br>
(※4)qr_codeフォルダ配下に、dataフォルダ配下に配置したCSVファイルを元に生成されたQRコードが生成され格納されます。詳しい仕様は後述のxxxxxxxxxxxxxを参考にしてください。<br>

### `setting.py`の使用方法(QRコード生成に関する設定)
- QRコードのバージョン (QR_VERSION)<br>
  - デフォルト値：1<br>
  - [(参考)QRコードのバージョンについて](https://www.qrcode.com/about/version.html)
- エラー訂正レベル (ERROR_CORRECTION_LEVEL)<br>
  - デフォルト値：Q<br>
  - [(参考)エラー訂正レベルについて](https://www.mediaseek.co.jp/barcode/10908/#:~:text=QR%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AB%E3%81%AF%E8%AA%A4%E3%82%8A,L%E3%81%A8%E3%81%AA%E3%81%A3%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82)
- QRコードの大きさ (BOX_SIZE)<br>
  - デフォルト値：10 (1つのドットが10ピクセル四方の大きさ)
- 境界線のサイズ (BORDER_SIZE)<br>
  - デフォルト値：4
- QRコードの色 (QR_COLOR)<br>
  - 16進数のRGB(#rrggbb)の形式で入力<br>
  - デフォルト：黒`#000000`
- QRコードの背景色 (QR_BACKGROUND_COLOR)<br>
  - 16進数のRGB(#rrggbb)の形式で入力<br>
  - デフォルト：白`#FFFFFF`
- 背景透過(任意) (QR_BACKGROUND_TRANSPARENT)<br>
  - False：背景透過しない<br>
  - True：背景透過する<br>
  - デフォルト：False
(※)上記以外の定数については編集厳禁です。

### dataフォルダに関するルール
- 配置したCSVファイル内のデータを元にQRコードを生成します。<br>
- 複数ファイル配置可能です。<br>
- 原則として、QRコードに変換したいCSVファイルのみをdataフォルダ配下に配置してください。<br>
(1回の実行でdataフォルダ配下全てのCSVファイルに対してQRコード生成のプログラムが走るので、既にQRコードに変換済のCSVファイルやその他意図しないファイルの配置に注意してください。)<br>

### CSVファイルのルール
- ヘッダ<br>
  - 行数,ファイル名,URL
- 行数<br>
  - 欠番なく1から記述してください。参考：下記のCSVファイル例<br>
- ファイル名<br>
  - 生成するQRコードのファイル名になります。<br>
  - ファイル名の末尾に`.png`を必ずつけてください。参考：下記のCSVファイル例<br>
- URL
  - パラメータも含めた完全なURLを記述してください。参考：下記のCSVファイル例<br>
- その他
  - ファイル内に空行を入れないでください<br>
  - 1行目のヘッダに何も書き加えないでください<br>
  - 行数、ファイル名、URL以外の情報を書き加えないでください(2行目以降)<br>
  - カンマの後にスペースを入れる必要はありません。参考：下記のCSVファイル例<br>

### CSVファイル例
```csv
行数,ファイル名,URL
1,田中太郎.png,https://example.com/?parameter_a=1?parameter_b=2
2,鈴木直美.png,https://example.com/?parameter_a=4
3,田中花子.png,https://example.com/?parameter_b=2?parameter_c=7?parameter_d=3?
.....
```

### imgフォルダに関するルール
- QRコードの中央に画像を配置したい場合は、imgディレクトリ配下に画像を挿入してください<br>
- imgフォルダ配下に何も画像を配置しない場合は、通常のQRコードが生成されます。<br>
- 画像を配置する場合、拡張子は必ず`.png`にしてください。<br>
- 配置する画像は1枚のみにしてください。2枚以上は配置できません。<br>
- 背景透過かつQRコードの中央に画像を配置したい場合は、imgフォルダに置く画像も背景透過したものを配置してください。

### qr_codeフォルダに関するルール
TODO: ディレクトリ分割について
TODO: 途中再開オプション時の出力について
TODO: ナンバーオプション時の出力について
TODO: オプション併用時の出力について
TODO: dataフォルダにcsvファイルが1つor複数の場合
TODO: 上書き保存・1回目通常出力→2回目ナンバーオプションの場合同じディレクトリ配下に名前が違うが同じファイルが保存される場合

## 実行
TODO: 通常
TODO: 途中再開オプション
TODO: ナンバーオプション
TODO: オプション併用

--- 


<b>《実行》</b>

実行コマンド
```
PYTHONPATH=. python src/read_csv.py
```

実行後、qr_codeフォルダ内にCSVファイルごとにサブフォルダが生成され、その中にデータとsetting.pyで指定したQRコードの設定をもとに生成されたQRコードの画像ファイルが格納されます。

<br>

## ドキュメント
- [簡易モジュール構成図・シーケンス図](https://drive.google.com/file/d/1QVUi4KcGqufxJIqEsboudCzGMNTTiXNh/view?usp=sharing)
