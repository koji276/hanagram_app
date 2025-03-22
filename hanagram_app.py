import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import copy  # ★ 追加

#############################################
# 三角形描画
#############################################
def draw_triangle(ax, x, y, direction='U', value=None, color='white'):
    height = np.sqrt(3) / 2
    if direction == 'U':
        points = np.array([
            [x, y],
            [x + 0.5, y + height],
            [x + 1, y]
        ])
    else:
        points = np.array([
            [x, y + height],
            [x + 0.5, y],
            [x + 1, y + height]
        ])

    polygon = plt.Polygon(points, edgecolor='black', facecolor=color)
    ax.add_patch(polygon)

    # 中央に数字を表示
    if value is not None:
        cx = x + 0.5
        cy = y + height / 2
        ax.text(cx, cy, str(value), fontsize=14, ha='center', va='center')

#############################################
# ボード描画 (初期値セル=薄青, 選択セル=黄, 他=白)
#############################################
def draw_board(board_values, selected_pos, initial_board_values):
    fig, ax = plt.subplots(figsize=(8, 8))

    board_structure = [
        ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
    ]
    height = np.sqrt(3) / 2

    for r_idx, row_data in enumerate(board_structure):
        for c_idx, cell in enumerate(row_data):
            if cell != 'N':
                x_offset = c_idx * 0.5
                y_offset = (5 - r_idx) * height
                value = board_values[r_idx][c_idx]

                # 色分けロジック
                if initial_board_values[r_idx][c_idx] is not None:
                    color = 'lightblue'   # 初期値(変更不可)
                elif (r_idx, c_idx) == selected_pos:
                    color = 'yellow'      # 選択中のセル
                else:
                    color = 'white'       # 通常セル（ユーザーが入力可）

                draw_triangle(ax, x_offset, y_offset, direction=cell,
                              value=value, color=color)

    # --- ラベル(A〜L)配置 ---
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

    for label, (r, c) in label_positions.items():
        x_lab = c * 0.5
        y_lab = (5 - r) * height
        dx, dy = label_shifts.get(label, (0,0))
        x_lab += dx
        y_lab += dy
        ax.text(x_lab, y_lab, label, color="red", fontsize=16, ha="center", va="center")

    ax.set_xlim(-2, 7)
    ax.set_ylim(-2, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

#############################################
# セッション初期化
#############################################
if 'board_values' not in st.session_state:
    st.session_state.board_values = [[None]*9 for _ in range(6)]

if 'initial_board_values' not in st.session_state:
    st.session_state.initial_board_values = [[None]*9 for _ in range(6)]

#############################################
# タイトル
#############################################
st.title('Hanagramアプリ（初期値=薄青, 選択=黄, 他=白）')

#############################################
# 列(A～L)＆番号(0～8) 選択
#############################################
lines_map = {
    "A": [(0,4),(0,3),(1,3),(1,2),(2,2),(2,1),(3,1),(3,0),(4,0)],
    "B": [(0,5),(1,5),(1,4),(2,4),(2,3),(3,3),(3,2),(4,2),(4,1)],
    "C": [(1,7),(1,6),(2,6),(2,5),(3,5),(3,4),(4,4),(4,3),(5,3)],
    "D": [(1,8),(2,8),(2,7),(3,7),(3,6),(4,6),(4,5),(5,5),(5,4)],
    "E": [(4,8),(3,8),(3,7),(2,7),(2,6),(1,6),(1,5),(0,5),(0,4)],
    "F": [(4,7),(4,6),(3,6),(3,5),(2,5),(2,4),(1,4),(1,3),(0,3)],
    "G": [(5,5),(4,5),(4,4),(3,4),(3,3),(2,3),(2,2),(1,2),(1,1)],
    "H": [(5,4),(5,3),(4,3),(4,2),(3,2),(3,1),(2,1),(2,0),(1,0)],
    "I": [(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8)],
    "J": [(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8)],
    "K": [(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8)],
    "L": [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)]
}

col_letter = st.selectbox("列(A～L)を選択", list(lines_map.keys()))
pos_index = st.selectbox("番号(0～8)を選択", list(range(9)))
(row, col) = lines_map[col_letter][pos_index]

#############################################
# 数字を選んで入力
#############################################
number = st.selectbox("数字を選んでください", [None,0,1,2,3,4,5,6,7,8,9])

if st.button('数字をセルに入力'):
    board_structure = [
        ['N','N','N','U','D','U','N','N','N'],
        ['U','D','U','D','U','D','U','D','U'],
        ['D','U','D','U','D','U','D','U','D'],
        ['U','D','U','D','U','D','U','D','U'],
        ['D','U','D','U','D','U','D','U','D'],
        ['N','N','N','D','U','D','N','N','N'],
    ]
    if board_structure[row][col] == 'N':
        st.warning('ここはセルが存在しません。')
    else:
        # 初期値セルは変更不可
        if st.session_state.initial_board_values[row][col] is not None:
            st.warning('このセルは初期値なので変更できません。')
        else:
            st.session_state.board_values[row][col] = number

#############################################
# ボード描画
#############################################
draw_board(st.session_state.board_values, (row, col), st.session_state.initial_board_values)

#############################################
# 重複チェックや完成判定など
#############################################
def generate_combinations():
    board_structure = [
        ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
    ]
    combos = {
        '横': [],
        '斜め_右上から左下': [],
        '斜め_左上から右下': [],
    }
    # 横方向 (4行分)
    for r_idx, row_data in enumerate(board_structure):
        temp_row = []
        for c_idx, cell in enumerate(row_data):
            if cell != 'N':
                temp_row.append((r_idx,c_idx))
        if len(temp_row) > 3:
            combos['横'].append(temp_row)

    combos['斜め_右上から左下'] = [
        [(0,4),(0,3),(1,3),(1,2),(2,2),(2,1),(3,1),(3,0),(4,0)],
        [(0,5),(1,5),(1,4),(2,4),(2,3),(3,3),(3,2),(4,2),(4,1)],
        [(1,7),(1,6),(2,6),(2,5),(3,5),(3,4),(4,4),(4,3),(5,3)],
        [(1,8),(2,8),(2,7),(3,7),(3,6),(4,6),(4,5),(5,5),(5,4)]
    ]
    combos['斜め_左上から右下'] = [
        [(0,4),(0,5),(1,5),(1,6),(2,6),(2,7),(3,7),(3,8),(4,8)],
        [(0,3),(1,3),(1,4),(2,4),(2,5),(3,5),(3,6),(4,6),(4,7)],
        [(1,1),(1,2),(2,2),(2,3),(3,3),(3,4),(4,4),(4,5),(5,5)],
        [(1,0),(2,0),(2,1),(3,1),(3,2),(4,2),(4,3),(5,3),(5,4)]
    ]
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
            if len(set(digits)) != 9:  # 重複チェック
                return False
    return True

combinations = generate_combinations()
st.subheader("12列の組み合わせ確認（テスト表示）")
for direction, lines in combinations.items():
    st.write(f"### {direction}")
    for idx, line in enumerate(lines):
        st.write(f"{direction} - 列{idx+1}: {line}")

st.subheader("🔎 数字の重複チェック結果")
dup_found, dup_info = check_duplicates(st.session_state.board_values, combinations)
if dup_found:
    st.error("⚠️ 重複があります。")
    for info in dup_info:
        st.write(info)
else:
    st.success("✅ 現在、重複はありません。")

if check_all_lines_completed(st.session_state.board_values, combinations):
    st.balloons()
    st.success("🎉 すべてのラインが完成しました！")

#############################################
# CSV読込用関数・読み込み処理
#############################################
def load_puzzle_from_csv(filename):
    df = pd.read_csv(filename, header=None)
    puzzle_data = df.where(pd.notnull(df), None).values.tolist()
    for r_idx, row_data in enumerate(puzzle_data):
        for c_idx, val in enumerate(row_data):
            if pd.notnull(val):
                puzzle_data[r_idx][c_idx] = int(val)
            else:
                puzzle_data[r_idx][c_idx] = None
    return puzzle_data

puzzle_folder = 'puzzles'
puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith('.csv')]
if puzzle_files:
    selected_puzzle_file = st.selectbox('🔍 パズルを選択', puzzle_files)
    if st.button('選択したパズルを読み込み'):
        puzzle_path = os.path.join(puzzle_folder, selected_puzzle_file)
        loaded_puzzle = load_puzzle_from_csv(puzzle_path)

        # ▼▼▼ ここを修正 ▼▼▼
        # 以前は同じリスト参照を代入していた
        # st.session_state.board_values = loaded_puzzle
        # st.session_state.initial_board_values = loaded_puzzle

        # deep copyを使って、初期値とユーザ入力用を分離
        st.session_state.board_values = copy.deepcopy(loaded_puzzle)
        st.session_state.initial_board_values = copy.deepcopy(loaded_puzzle)
        # ▲▲▲ ここまで修正 ▲▲▲

        st.success(f"{selected_puzzle_file} を読み込みました！")
else:
    st.warning("puzzlesフォルダにCSVファイルがありません。")

