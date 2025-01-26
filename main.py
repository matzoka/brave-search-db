import streamlit as st
import pandas as pd
import requests
import os
import io
from dotenv import load_dotenv

# 環境変数の読み込み
try:
    load_dotenv()

    API_KEY = os.getenv('SEARCH_API_KEY')
except:
    API_KEY = None

# SearchAPI.io設定
if not API_KEY:
    try:
        API_KEY = st.secrets['secret']['SEARCH_API_KEY']
    except:
        API_KEY = None

API_URL = 'https://www.searchapi.io/api/v1/search'

def searchAPI_search(query, num_results):
    """Search APIを使用して検索を実行"""
    headers = {
        'Accept': 'application/json',
    }

    params = {
        'engine': 'google',
        'q': query,
        'num': str(num_results + 10),  # 要求数+10を指定して確実に必要な件数を確保
        'gl': 'jp',  # 地域を日本に設定
        'hl': 'ja',  # インターフェース言語を日本語に設定
        'lr': 'lang_ja',  # 検索結果を日本語に限定
        'api_key': API_KEY
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # エラーレスポンスの場合は例外を発生

        data = response.json()
        results = []

        for item in data.get('organic_results', [])[:num_results]:  # APIからの結果をそのまま使用
            results.append({
                'title': item.get('title', 'No Title'),
                'description': item.get('snippet', 'No Description'),
                'url': item.get('link', 'No URL')
            })

        return results

    except requests.exceptions.RequestException as e:
        raise Exception(f"APIリクエストに失敗しました: {str(e)}")
    except Exception as e:
        raise Exception(f"検索結果の処理に失敗しました: {str(e)}")

# Streamlit UI
st.title("検索結果エクスポーター")
st.write("検索キーワードを入力して検索結果を取得します")

# SearchAPI.io API_KEYが設定されているか確認
if not API_KEY:
    st.error("⚠️ SearchAPI.io API Keyが設定されていません。")
    st.info("💡 ローカル環境: .envファイルにSEARCH_API_KEY=あなたのAPIキー を設定")
    st.info("💡 Streamlit Cloud: Settings > Secrets に 'secret.SEARCH_API_KEY' を設定")
    st.stop()

# 検索オプションの配置を2カラムに分ける
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input(
        "検索キーワード",
        placeholder="検索キーワードを入力してください",
        help="""検索キーワードの指定方法：

• 除外ワード指定：キーワードの前に「-」を付ける\n  例：東京 -大阪（「東京」を含み「大阪」を含まない）
• サイト除外：-site:ドメイン名\n
  例：Python -site:stackoverflow.com

"""
    )
with col2:
    num_results = st.number_input("取得件数", min_value=1, value=50, step=10, help="10件単位で調整できます")

if st.button("検索実行", type="primary"):
    if search_query:
        with st.spinner("検索中..."):
            try:
                search_results = searchAPI_search(search_query, num_results)

                if search_results:
                    # 結果をDataFrameに変換
                    df_data = [
                        {
                            "Rank": i + 1,
                            "Title": result["title"],
                            "URL": result["url"],
                            "Description": result["description"]
                        }
                        for i, result in enumerate(search_results)
                    ]
                    df = pd.DataFrame(df_data)
                    # セッションステートに保存
                    st.session_state['search_results_df'] = df
                    st.session_state['last_query'] = search_query
                else:
                    st.warning("🔍 検索結果が見つかりませんでした。検索キーワードを変更してお試しください。")
                    st.info("💡 TIP: スペースで区切って複数のキーワードを指定することもできます")

            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
    else:
        st.warning("⚠️ 検索キーワードを入力してください")

# 検索結果が保存されている場合、出力オプションを表示
if 'search_results_df' in st.session_state:
    df = st.session_state['search_results_df']
    search_query = st.session_state['last_query']

    st.success(f"✨ {len(df)}件の結果が見つかりました")

    # データフレームの表示を改善
    st.dataframe(
        df,
        column_config={
            "Rank": st.column_config.NumberColumn("順位"),
            "Title": st.column_config.TextColumn("タイトル"),
            "URL": st.column_config.LinkColumn("URL"),
            "Description": st.column_config.TextColumn("説明")
        },
        hide_index=True
    )

    # ファイル形式の選択（デフォルトはEXCEL）
    file_format = st.radio(
        "出力形式を選択",
        ["EXCEL", "CSV"],
        index=0,  # デフォルトでEXCELを選択
        horizontal=True  # 横並びに表示
    )

    base_filename = f"search_results_{search_query.replace(' ', '_')[:30]}"

    if file_format == "EXCEL":
        # Excel形式で出力
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='検索結果')
        excel_data = excel_buffer.getvalue()
        st.download_button(
            label="📥 Excelダウンロード",
            data=excel_data,
            file_name=f"{base_filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        # CSV形式で出力（BOMを追加してExcelで文字化けを防ぐ）
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 CSVダウンロード",
            data=csv_data,
            file_name=f"{base_filename}.csv",
            mime="text/csv"
        )

# 使い方と注意事項
with st.expander("💡 使い方と注意事項"):
    st.markdown("""
    ### 使い方
    1. 検索キーワードを入力
    2. 取得件数を選択
    3. 「検索実行」ボタンをクリック
    4. 出力形式（EXCEL/CSV）を選択してダウンロード

    ### 注意事項
    - .envファイルに searchapi.io APIキーを設定してください
    """)
