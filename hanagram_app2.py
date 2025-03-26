import streamlit as st
import pandas as pd
import os
import numpy as np
import copy
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

def load_selected_puzzle():
    puzzle_path = os.path.join(puzzle_folder, st.session_state.selected_file)
    loaded_puzzle = load_puzzle_from_csv(puzzle_path)
    st.session_state.board_values = copy.deepcopy(loaded_puzzle)
    st.session_state.initial_board_values = copy.deepcopy(loaded_puzzle)
    st.session_state.highlight_digits = []
    st.session_state.selected_pos = (None, None)

    # ▼ここを追加
    st.write("読み込んだパズルデータ:", st.session_state.board_values)

    st.success(f"{st.session_state.selected_file} を読み込みました！")


#############################################
# ページレイアウト設定 (任意)
#############################################
st.set_page_config(page_title="Hanagram with Plotly", layout="wide")

#############################################
# セッション初期化
#############################################
if 'board_values' not in st.session_state:
    st.session_state.board_values = [[None]*9 for _ in range(6)]

if 'initial_board_values' not in st.session_state:
    st.session_state.initial_board_values = [[None]*9 for _ in range(6)]

if 'highlight_digits' not in st.session_state:
    st.session_state.highlight_digits = []

# 「ユーザーがクリック/タップしたセル」の座標を保持しておく
if 'selected_pos' not in st.session_state:
    st.session_state.selected_pos = (None, None)

#############################################
# タイトル
#############################################
st.title('Hanagramアプリ (Plotly版)  https://www.hanagram.net')

#############################################
# 盤面構造 (三角形の向き) 定義
#############################################
board_structure = [
    ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
    ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
    ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
    ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
    ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
    ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
]
height = np.sqrt(3) / 2

#############################################
# Plotly で三角形セルを描画し、クリックイベントを拾う関数
#############################################
def draw_board_plotly(board_values, selected_pos, initial_board_values,
                      puzzle_completed=False, highlight_digits=None):
    fig = go.Figure()
    for r_idx, row_data in enumerate(board_structure):
        for c_idx, cell_dir in enumerate(row_data):
            if cell_dir == 'N':
                continue
            x_offset = c_idx * 0.5
            y_offset = (5 - r_idx) * height
            if cell_dir == 'U':
                p1 = (x_offset,       y_offset)
                p2 = (x_offset+0.5,  y_offset+height)
                p3 = (x_offset+1.0,  y_offset)
            else:
                p1 = (x_offset,       y_offset+height)
                p2 = (x_offset+0.5,  y_offset)
                p3 = (x_offset+1.0,  y_offset+height)
            val = board_values[r_idx][c_idx]

            # 色分け
            if initial_board_values[r_idx][c_idx] is not None:
                color = 'lightblue'
            elif (r_idx, c_idx) == selected_pos:
                color = 'yellow'
            else:
                color = 'white'
            if puzzle_completed and highlight_digits and (val in highlight_digits):
                color = 'pink'

            path_d = f"M {p1[0]},{p1[1]} L {p2[0]},{p2[1]} L {p3[0]},{p3[1]} Z"
            shape_name = f"cell_{r_idx}_{c_idx}"
            fig.add_shape(
                type="path",
                path=path_d,
                fillcolor=color,
                line=dict(color="black"),
                name=shape_name
                layer='below'  # <-- これを追加！
            )

            cx = (p1[0] + p2[0] + p3[0]) / 3.0
            cy = (p1[1] + p2[1] + p3[1]) / 3.0
            text_val = str(val) if val is not None else ""
            fig.add_trace(go.Scatter(
                x=[cx],
                y=[cy],
                text=[text_val],
                #mode="markers+text",  # ← markersを足す
                # marker=dict(size=30, color="rgba(0,0,0,0)"),  # 透明マーカー

                mode="markers+text",  # 大きな円＋テキスト
                marker=dict(size=30, color="rgba(255,0,0,0.3)"),  # 赤い半透明マーカー
                
                textfont=dict(size=16, color="black"),
                textposition="middle center",
                name=shape_name,
                customdata=[(r_idx, c_idx)],
                hoverinfo="skip"
            ))

    # ラベル(A～L)を描画する(散布図トレース or shape)
    label_positions = {
        "A": (-1, 4),
        "B": (1, 6),
        "C": (1, 7),
        "D": (2, 9),
        "E": (4, 9),
        "F": (5, 7),
        "G": (5, 6),
        "H": (6, 4),
        "I": (4, -1),
        "J": (3, -1),
        "K": (2, -1),
        "L": (1, -1),
    }
    label_shifts = {
        "A": (0.5, 0.3), "B": (0.5, 1.5), "C": (0.5, 1.1), "D": (0.5, 1.4),
        "E": (0.5, 0.4), "F": (0.5, 0.6), "G": (0.5, 0.2), "H": (0.5, 0.5),
        "I": (0.1, 0.4), "J": (0.1, 0.4), "K": (0.1, 0.4), "L": (0.1, 0.4),
    }

    # 別トレースでテキスト描画
    label_x = []
    label_y = []
    label_text = []
    for label, (r, c) in label_positions.items():
        x_lab = c * 0.5
        y_lab = (5 - r) * height
        dx, dy = label_shifts.get(label, (0,0))
        x_lab += dx
        y_lab += dy

        label_x.append(x_lab)
        label_y.append(y_lab)
        label_text.append(label)

    fig.add_trace(
        go.Scatter(
            x=label_x,
            y=label_y,
            text=label_text,
            mode="text",
            textfont=dict(size=16, color="red"),
            hoverinfo="skip",
            name="labels"
        )
    )

    # レイアウト調整
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout(
        width=700,
        height=700,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        dragmode=False
    )

    # ここで plotly_events を呼び出す → 余計な引数は付けない
    selected_points = plotly_events(
        fig,
        click_event=True,
        hover_event=False,
        select_event=False,
    )

    st.write("selected_points:", selected_points)  # ← デバッグ表示

    clicked_cell = None
    if selected_points:
        event = selected_points[-1]
        if 'customdata' in event and isinstance(event['customdata'], (list, tuple)):
            if len(event['customdata']) == 2:
                clicked_cell = (event['customdata'][0], event['customdata'][1])
    return clicked_cell

#############################################
# 重複チェックや完成判定の関数
#############################################
def generate_combinations():
    combos = {
        '斜め_右上から左下': [
            [(0,4),(0,3),(1,3),(1,2),(2,2),(2,1),(3,1),(3,0),(4,0)],
            [(0,5),(1,5),(1,4),(2,4),(2,3),(3,3),(3,2),(4,2),(4,1)],
            [(1,7),(1,6),(2,6),(2,5),(3,5),(3,4),(4,4),(4,3),(5,3)],
            [(1,8),(2,8),(2,7),(3,7),(3,6),(4,6),(4,5),(5,5),(5,4)]
        ],
        '斜め_右下から左上': [
            [(4,8),(3,8),(3,7),(2,7),(2,6),(1,6),(1,5),(0,5),(0,4)],
            [(4,7),(4,6),(3,6),(3,5),(2,5),(2,4),(1,4),(1,3),(0,3)],
            [(5,5),(4,5),(4,4),(3,4),(3,3),(2,3),(2,2),(1,2),(1,1)],
            [(5,4),(5,3),(4,3),(4,2),(3,2),(3,1),(2,1),(2,0),(1,0)]
        ],
        '横方向_左から右': [
            [(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8)],
            [(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8)],
            [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8)],
            [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)]
        ],
    }
    return combos

def check_duplicates(board_values, combos):
    dup_found = False
    dup_info = []
    for direction, lines in combos.items():
        for idx, line in enumerate(lines):
            nums_in_line = []
            for (r,c) in line:
                val = board_values[r][c]
                if val is not None:
                    nums_in_line.append(val)
            dups = set([num for num in nums_in_line if nums_in_line.count(num) > 1])
            if dups:
                dup_found = True
                dup_info.append(f"{direction} - 列{idx+1} 重複: {dups}")
    return dup_found, dup_info

def check_all_lines_completed(board_values, combos):
    for direction, lines in combos.items():
        for line in lines:
            digits = []
            for (r,c) in line:
                val = board_values[r][c]
                if val is None:
                    return False
                digits.append(val)
            if len(set(digits)) != 9:
                return False
    return True

#############################################
# CSV読込用関数
#############################################
def load_puzzle_from_csv(filename):
    df = pd.read_csv(filename, header=None)
    # df の欠損値(NaN)を None に変換
    puzzle_data = df.where(pd.notnull(df), None).values.tolist()

    for r_idx, row_data in enumerate(puzzle_data):
        for c_idx, val in enumerate(row_data):
            if val is not None:
                try:
                    puzzle_data[r_idx][c_idx] = int(val)
                except ValueError:
                    # 変換できない値は None に置き換え
                    puzzle_data[r_idx][c_idx] = None
    return puzzle_data


#############################################
# パズル読み込みUI
#############################################
puzzle_folder = 'puzzles'
puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith('.csv')]

if puzzle_files:
    st.selectbox(
        label='🔍 パズルを選択',
        options=puzzle_files,
        key="selected_file"
    )

    def load_selected_puzzle():
        puzzle_path = os.path.join(puzzle_folder, st.session_state.selected_file)
        loaded_puzzle = load_puzzle_from_csv(puzzle_path)
        st.session_state.board_values = copy.deepcopy(loaded_puzzle)
        st.session_state.initial_board_values = copy.deepcopy(loaded_puzzle)
        st.session_state.highlight_digits = []
        st.session_state.selected_pos = (None, None)
        st.success(f"{st.session_state.selected_file} を読み込みました！")

    if st.button('選択したパズルを読み込み', on_click=load_selected_puzzle):
        pass
else:
    st.warning("puzzles フォルダに CSV ファイルがありません。")

#############################################
# メインロジック
#############################################
# 1) Plotly で盤面を描画 & クリックされたセルを取得
clicked_cell = draw_board_plotly(
    board_values = st.session_state.board_values,
    selected_pos = st.session_state.selected_pos,
    initial_board_values = st.session_state.initial_board_values,
    puzzle_completed = False,  # 一旦後で判定
    highlight_digits = st.session_state.highlight_digits
)

# 2) もしクリックされたら、選択セルを更新
if clicked_cell is not None:
    st.session_state.selected_pos = clicked_cell

# 3) 数字選択 UI → “選択中セル” に入力
st.write(f"現在の選択セル: {st.session_state.selected_pos}")
number = st.selectbox("数字を選んでください", [None,0,1,2,3,4,5,6,7,8,9])
if st.button('数字をセルに入力'):
    r, c = st.session_state.selected_pos
    if r is None or c is None:
        st.warning("セルが選択されていません。")
    else:
        # 初期値セルは変更不可
        if st.session_state.initial_board_values[r][c] is not None:
            st.warning('このセルは初期値なので変更できません。')
        else:
            st.session_state.board_values[r][c] = number

# 4) 重複チェック & 完成判定
combinations = generate_combinations()
dup_found, dup_info = check_duplicates(st.session_state.board_values, combinations)
puzzle_completed = check_all_lines_completed(st.session_state.board_values, combinations)

st.subheader("🔎 数字の重複チェック結果")
if dup_found:
    st.error("⚠️ 重複があります。")
    for info in dup_info:
        st.write(info)
else:
    st.success("✅ 現在、重複はありません。")

# 5) パズルが完成していればハイライト UI を表示
if puzzle_completed:
    st.balloons()
    st.success("🎉 すべてのラインが完成しました！")
    st.subheader("🌸 花柄(ハナグラム)表示オプション")
    selected_digits = st.multiselect(
        "ピンク色でハイライトする数字を選んでください（複数選択可）",
        [0,1,2,3,4,5,6,7,8,9],
        default = st.session_state.highlight_digits
    )
    if st.button("表示"):
        st.session_state.highlight_digits = selected_digits

    # いったん再度描画 (完了後のハイライト表示)  
    # クリックイベントは不要なので、下記は描画だけでもOK
    draw_board_plotly(
        board_values = st.session_state.board_values,
        selected_pos = st.session_state.selected_pos,
        initial_board_values = st.session_state.initial_board_values,
        puzzle_completed = puzzle_completed,
        highlight_digits = st.session_state.highlight_digits
    )
else:
    st.info("パズルが完成すると、選択した数字をピンクでハイライトできます。")

