import streamlit as st
import pandas as pd
import requests
import os
import io
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Brave Search API設定
API_KEY = os.getenv('BRAVE_API_KEY')
API_URL = 'https://api.search.brave.com/res/v1/web/search'

def brave_search(query, num_results):
    """Brave Search APIを使用して検索を実行"""
    headers = {
        'X-Subscription-Token': API_KEY,
        'Accept': 'application/json',
    }

    params = {
        'q': query,
        'count': num_results
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # エラーレスポンスの場合は例外を発生

        data = response.json()
        results = []

        for item in data.get('web', {}).get('results', []):
            results.append({
                'title': item.get('title', ''),
                'description': item.get('description', ''),
                'url': item.get('url', '')
            })

        return results

    except requests.exceptions.RequestException as e:
        raise Exception(f"APIリクエストに失敗しました: {str(e)}")
    except Exception as e:
        raise Exception(f"検索結果の処理に失敗しました: {str(e)}")

# Streamlit UI
st.title("検索結果エクスポーター")
st.write("検索キーワードを入力して検索結果を取得します")

# API_KEYが設定されているか確認
if not API_KEY:
    st.error("⚠️ Brave Search API Keyが設定されていません。.envファイルを確認してください。")
    st.info("💡 .envファイルにBRAVE_API_KEY=あなたのAPIキー を設定してください。")
    st.stop()

# 検索オプションの配置を2カラムに分ける
col1, col2 = st.columns(2)
with col1:
    search_query = st.text_input("検索キーワード", placeholder="検索キーワードを入力してください")
with col2:
    num_results = st.number_input("取得件数", min_value=1, max_value=50, value=10, help="最大50件まで取得できます")

if st.button("検索実行", type="primary"):
    if search_query:
        with st.spinner("検索中..."):
            try:
                search_results = brave_search(search_query, num_results)

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

                else:
                    st.warning("🔍 検索結果が見つかりませんでした。検索キーワードを変更してお試しください。")
                    st.info("💡 TIP: スペースで区切って複数のキーワードを指定することもできます")

            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
    else:
        st.warning("⚠️ 検索キーワードを入力してください")

# 使い方と注意事項
with st.expander("💡 使い方と注意事項"):
    st.markdown("""
    ### 使い方
    1. .envファイルにBrave Search APIキーを設定
    2. 検索キーワードを入力
    3. 取得件数を選択（最大50件）
    4. 「検索実行」ボタンをクリック
    5. 出力形式（EXCEL/CSV）を選択してダウンロード

    ### 注意事項
    - APIキーは.envファイルで管理します
    - 検索結果はEXCELまたはCSV形式でダウンロード可能です
    - 日本語検索に対応しています
    """)
