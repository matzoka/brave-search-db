# Brave Search Results Exporter

Brave Search APIを使用して検索結果をCSVファイルとしてエクスポートできるStreamlitアプリケーションです。

## 機能

- Brave Search APIを使用した検索
- 任意の件数で検索結果を取得可能
- 10件単位での簡単な件数調整
- 検索結果のリアルタイム表示
- Excel/CSV形式でのエクスポート（UTF-8 with BOM対応）
- 日本語検索完全対応

## 必要要件

- Python 3.8以上
- Brave Search APIキー

## インストール

```bash
git clone https://github.com/[your-username]/brave-search-db.git
cd brave-search-db
pip install -r requirements.txt
```

## 環境設定

### ローカル環境での設定

1. `.env`ファイルをプロジェクトのルートディレクトリに作成
2. 以下の内容を追加：

```
BRAVE_API_KEY=あなたのAPIキー
```

### Streamlit Cloudでの設定

1. [Streamlit Cloud](https://streamlit.io/cloud)にデプロイ
2. アプリの設定画面を開く
3. Settings > Secrets セクションで以下を設定：
   ```toml
   [secret]
   BRAVE_API_KEY = "あなたのAPIキー"
   ```

## 使用方法

1. アプリケーションを起動：
```bash
streamlit run main.py
```

2. Webブラウザが開き、アプリケーションにアクセスできます
3. 検索キーワードを入力し、取得件数を選択（10件単位で調整可能）
4. 「検索実行」ボタンをクリック
5. 出力形式（EXCEL/CSV）を選択してダウンロード

## 注意事項

- ローカル環境では`.env`ファイル、Streamlit Cloudでは Secrets で APIキーを管理
- APIキーはGitHubには公開しないようご注意ください
- API利用制限については[Brave Search API](https://brave.com/search/api/)の利用規約をご確認ください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)をご覧ください。
