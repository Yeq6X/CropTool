# Image Crop Tool

## 概要
このツールは、画像処理のためのシンプルなアプリケーションです。画像を選択し、クロップやカラー背景の適用などの処理を行うことができます。
![image](https://github.com/user-attachments/assets/c41ba500-214e-477c-a9f0-b3953f986621)

## 主な機能
- 画像の閲覧・ナビゲーション
- 四隅選択モードと中心点選択モードによる画像のクロップ
- 背景色の選択と適用
- 処理済み画像の保存
- 画像のスキップ（無視）機能

## 必要環境
- Python 3.x
- PIL (Pillow)
- tkinter (通常はPythonに標準で含まれています)

## インストールと実行方法
1. リポジトリをクローンまたはダウンロードします。
   ```
   git clone [リポジトリURL]
   ```
2. launch.bat を実行すると、自動的に仮想環境のセットアップと必要なパッケージのインストールが行われます。
   ```
   launch.bat
   ```
   または、手動で以下のコマンドを実行します：
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

## 使用方法
1. アプリケーションを起動すると、入力フォルダを選択するダイアログが表示されます。
2. 処理したい画像が含まれるフォルダを選択します。選択したフォルダ内に`output`フォルダが自動的に作成されます。
3. 画像が表示されたら、以下のホットキーとマウス操作を使用できます：

### ホットキー（初期設定）
以下のホットキーは`data/settings.json`で変更できます：
- **Space**: 次の画像へ移動
- **Shift + Space**: 前の画像へ移動
- **Ctrl + S**: 現在の画像を保存（選択した矩形領域が`output`フォルダに保存されます）
- **Ctrl + B**: 現在の画像をスキップ
- **R**: 四隅選択モードに切り替え（矩形領域の選択方法）
- **E**: 中心点選択モードに切り替え（矩形領域の選択方法）
- **S**: 背景色をカーソル位置から取得

### 設定のカスタマイズ
`data/settings.json`で以下の設定をカスタマイズできます：
- ホットキーの割り当て
- ウィンドウサイズ
- その他の動作設定

### マウス操作
- **左クリック + ドラッグ**: 矩形領域の選択
  - 四隅選択モード（R）: ドラッグで対角線上の2点を指定して矩形を選択
  - 中心点選択モード（E）: 最初のクリックで中心点を指定し、ドラッグで矩形のサイズを調整
- **右クリック**: カーソル位置の色を背景色として取得（Sキーと同じ機能）
- **マウスホイール**: 画像を縦方向にスクロール
- **Shift + マウスホイール**: 画像を横方向にスクロール
- **Ctrl + マウスホイール**: 画像の拡大/縮小

### 画像の切り抜きと保存
- 矩形選択した範囲が画像からはみ出した場合、はみ出した部分は設定した背景色で塗りつぶされます。
- 保存された画像は`output`フォルダに元のファイル名で保存されます。
- `output`フォルダには`progress.json`も自動的に作成され、処理状況が記録されます。

## 進捗管理
アプリケーションは、画像の処理状況を自動的に管理します。処理状況は選択したフォルダの`output`ディレクトリ内の`progress.json`ファイルに保存されます。

### progress.jsonの仕様
このファイルには以下の情報が記録されます：
```json
{
    "画像ファイル名": {
        "status": "処理状態",  // "completed", "incomplete", "ignored"
        "is_discarded": false, // 以前のファイルリストから削除された場合はtrue
    },
    ...
}
```

- **status**: 画像の処理状態
  - `completed`: 処理完了（Ctrl + Sで保存した場合のみ）。次回起動時にスキップされます。単に次の画像に進んだだけでは`completed`になりません。
  - `incomplete`: 未処理
  - `ignored`: スキップ済み。次回起動時にスキップされます。
- **is_discarded**: 以前のファイルリストから削除された（移動または削除された）場合に`true`になるフラグ

このファイルにより、アプリケーションを終了して再開した場合でも、前回の処理状況から継続することができます。`completed`または`ignored`ステータスのファイルは自動的にスキップされ、未処理（`incomplete`）のファイルのみが表示されます。

## プロジェクト構造
- **main.py**: アプリケーションのエントリポイント
- **models/**: データモデルを含むフォルダ
- **views/**: UIビューを含むフォルダ
- **viewmodels/**: ビューモデル（UIロジック）を含むフォルダ
- **utils/**: ユーティリティ関数を含むフォルダ
- **data/**: 設定と進捗データを保存するフォルダ

## ライセンス
Apache License 2.0

Copyright 2024 Toyofuku

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
