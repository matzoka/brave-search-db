# Brave Search Results Exporter

Brave Search APIを使用して検索結果をCSVファイルとしてエクスポートできるStreamlitアプリケーションです。

## 機能

- Brave Search APIを使用した検索
- 最大50件までの検索結果取得
- 検索結果のリアルタイム表示
- CSV形式でのエクスポート（UTF-8 with BOM対応）
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

1. `.env`ファイルをプロジェクトのルートディレクトリに作成
2. 以下の内容を追加：

```
BRAVE_API_KEY=あなたのAPIキー
```

## 使用方法

1. アプリケーションを起動：
```bash
streamlit run main.py
```

2. Webブラウザが開き、アプリケーションにアクセスできます
3. 検索キーワードを入力し、取得件数（1-50件）を選択
4. 「検索実行」ボタンをクリック
5. 結果を確認し、必要に応じてCSVをダウンロード

## 注意事項

- APIキーは`.env`ファイルで管理し、GitHubには公開しないようご注意ください
- API利用制限については[Brave Search API](https://brave.com/search/api/)の利用規約をご確認ください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)をご覧ください。
