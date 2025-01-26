# 🔍 SearchXplorer - 高度な検索を、シンプルに。

SearchXplorerは、Google検索を効率的に行い、結果を簡単にエクスポートできるツールです。
高度な検索オプションを直感的に使え、必要な情報をすばやく見つけることができます。

![SearchXplorer Screenshot](https://github.com/user-attachments/assets/9513907c-544f-455a-98cf-c10ab732977f)

## ✨ 特長

- **シンプルなUI** - 必要な機能だけを、使いやすく配置
- **スマートな検索** - エンターキーで即座に検索実行
- **柔軟な検索オプション** - 除外ワードやサイト指定に対応
- **カスタマイズ可能な取得件数** - 必要な件数を自由に指定
- **高速な結果表示** - リアルタイムでプレビュー
- **便利なエクスポート** - Excel/CSVで検索結果を保存
- **日本語検索に最適化** - 日本語コンテンツを正確に取得

## 🛠 必要要件

- Python 3.8以上
- Google Search APIキー

## 📦 インストール

```bash
git clone https://github.com/[your-username]/google-search.git
cd google-search
pip install -r requirements.txt
```

## ⚙️ 環境設定

### ローカル環境での設定

1. `.env`ファイルをプロジェクトのルートディレクトリに作成
2. 以下の内容を追加：

```
SEARCH_API_KEY=あなたのAPIキー
```

### Streamlit Cloudでの設定

1. [Streamlit Cloud](https://streamlit.io/cloud)にデプロイ
2. アプリの設定画面を開く
3. Settings > Secrets セクションで以下を設定：
   ```toml
   [secret]
   SEARCH_API_KEY = "あなたのAPIキー"
   ```

## 💡 使用方法

1. アプリケーションを起動：
```bash
streamlit run main.py
```

2. Webブラウザが開き、アプリケーションにアクセスできます
3. 検索キーワードを入力し、Enterキーを押すか取得件数を選択
4. 検索結果をその場でプレビュー
5. お好みの形式（EXCEL/CSV）でダウンロード

### 高度な検索テクニック

- **基本的な検索**: スペースで区切って複数のキーワードを指定
- **除外ワード指定**: キーワードの前に「-」を付ける（例: 東京 -大阪）
- **サイト除外**: -site:ドメイン名（例: Python -site:stackoverflow.com）

## ⚠️ 注意事項

- APIキーは`.env`ファイルまたはStreamlit Cloudの Secrets で安全に管理
- APIキーはGitHubには公開しないでください
- API利用制限は[Google Search API](https://www.searchapi.io/api/)の規約をご確認ください

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)をご覧ください。
