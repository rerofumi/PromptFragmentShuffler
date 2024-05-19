# PromptFragmentShuffler
Randomly generate prompts for image generation.

ランダムに選択された単語2つが追加された生成画像のうち、どちらが好みかをチョイスすることでプロンプトを伸ばしていけるツールです。

![App image](/Image/Screenshot_2024-05-19_a.jpg "app image")

## 必要なもの

- 実行環境
  - Python
    - Windows 版の Python 3.10 で作成
  - python pip モジュール
    - 以下を使用、pip で予め入れておくか venv を作ってそこの pip で install
    - gradio
    - requests
    - Pillow
  - ComfyUI 実行環境
    - ComfyUI を API 経由で呼び出すので、ComfyUI が動く環境を構築できること
    - API 経由で利用するのでドライブのどこに置いてあっても大丈夫
- 各種学習済みモデル
  - ComfyUI のワークフローモデル内で以下を使用
    - 必要に応じて同じものを揃えたり、自分の好みの奴に差し替える
  - SDXLモデル
    - AnythingXL_xl.safetensors

## インストール方法

1. PromptFragmentShuffler のリポジトリを clone する
2. PromptFragmentShuffler のディレクトリに移動し venv 環境を作成する
    
    Linux
    ```bash
    cd PromptFragmentShuffler
    python -m venv venv
    ./venv/bin/activate
    ```
    Windows
    ```powershell
    cd PromptFragmentShuffler
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3. PromptFragmentShuffler が使うモジュールを必要に応じてインストールする
    ```
    pip install -r requirements.txt
    ```

## 使い方

### 起動

1. ComfyUI を `127.0.0.1:8188` で待ち受けている状態で起動すること(通常起動)
2. ComfyUI GUI は使わないのでブラウザが起動しても、閉じてしまって良い
3. `python shuffler_ui.py` で起動、起動後ブラウザで `http://127.0.0.1:7860/` にアクセスする

### 設定

config.py 内にある設定を必要に応じて編集する、変更したら `shuffler_ui.py` を再起動すること
  - COMFYUI_USE_CHECKPOINT
    - ComfyUI で画像生成に使いたいチェックポイントファイルを指定する
    - 初期設定は "animagineXLV31_v31.safetensors"
    - ここに指定するファイルが `ComfyUI/models/checkpoints/` 以下にあること
  - COMFYUI_URL
    - ComfyUI API へのアクセスポイントを指定
    - ローカル PC 内に起動している時は修正しなくて良いはず

### 基本的な使い方

1. prompt, negative prompt を適切に設定する

2. サイコロボタンを押すことで全要素ランダムなプロンプトを生成する、編集の初期ベースとして利用できる

3. 初回、prompt を編集後、サイコロボタンで prompt を生成した後は必ず `Neither` ボタンを押して prompt の適用＆初回画像生成を行う

4. Operate は prompt をどう変化させるかの指定
    - add = Parts 種別の単語リストからランダムで抽出した単語を 1つ追加する
    - replace = Parts 種別の単語を 1つ消し、ランダムで抽出した単語に置き換える
    - remove = Parts 種別の単語からランダムで 1つ消す

5. Parts ランダムで操作したい単語の種別を指定する
    - positive = 高品質タグ
    - pose = ポーズ、仕草
    - composition = 構図
    - hairstyle = 髪型
    - expression = 表情
    - cloths = 衣装
    - accessory = 体に付けているアイテム、身体特徴
    - location = 背景、場所
    - props = 小物

6. Operate, Parts を設定して `Neither` ボタンをクリックすると prompt に対し 2つの単語を操作した 2枚の画像が表示される、これを見比べて好みの方の `A`, `B` ボタンを押すとその単語が prompt に適用され、次の単語＆画像生成に進む

7. もし A, B どちらの単語も好みではない場合は `Neither` ボタンを押すことで prompt をキープしたまま次の単語チョイスに進む

## カスタマイズ

- prompt 編集に使われる単語は `Collection/` ディレクトリの下にあるテキストファイルに書かれている
- 自分で良く使う単語や、不要な単語を追加削除してオリジナルな単語帳を作成しよう

## ライセンス

MIT license.

## 作者情報

rerofumi

## 変更履歴

- May.19.2024
    - first release
