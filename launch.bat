@echo off
chcp 65001 > nul

REM venvディレクトリが存在するか確認
IF NOT EXIST venv (
    echo.[仮想環境が見つかりません。新しく作成します...]
    python -m venv venv
)

REM venvをアクティベート
echo.[venvをアクティベートします...]
call venv\Scripts\activate.bat

REM requirements.txtが存在する場合、パッケージをインストール
IF EXIST requirements.txt (
    echo.[必要なパッケージをインストールします...]
    pip install -r requirements.txt
)

REM main.pyを実行
python main.py

REM 完了メッセージ
echo.[処理が完了しました。]
pause