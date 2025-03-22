import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#############################################
# 三角形描画
#############################################
def draw_triangle(ax, x, y, direction='U', value=None, color='white'):
    height = np.sqrt(3) / 2
    if direction == 'U':
        points = np.array([[x, y],
                           [x + 0.5, y + height],
                           [x + 1, y]])
    else:  # direction == 'D'
        points = np.array([[x, y + height],
                           [x + 0.5, y],
                           [x + 1, y + height]])

    polygon = plt.Polygon(points, edgecolor='black', facecolor=color)
    ax.add_patch(polygon)

    # 数値があれば三角形の中央に表示
    if value is not None:
        cx = x + 0.5
        cy = y + height / 2
        ax.text(cx, cy, str(value), fontsize=14, ha='center', va='center')


#############################################
# ボード描画
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
            if cell != 'N':  # マスがあるときのみ描画
                x_offset = c_idx * 0.5
                y_offset = (5 - r_idx) * height
                value = board_values[r_idx][c_idx]

                # --- 色分けロジック ---
                if initial_board_values[r_idx][c_idx] is not None:
                    # 初期値セルは薄青
                    color = 'lightblue'
                elif (r_idx, c_idx) == selected_pos:
                    # 選択中セルは黄色
                    color = 'yellow'
                else:
                    # それ以外のセルは白
                    color = 'white'

                draw_triangle(ax, x_offset, y_offset,
                              direction=cell, value=value, color=color)

    # --- ラベル(A～L)配置（任意） ---
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
        "A": (0.5, 0.3),
        "B": (0.5, 1.5),
        "C": (0.5, 1.1),
        "D": (0.5, 1.4),
        "E": (0.5, 0.4),
        "F": (0.5, 0.6),
        "G": (0.5, 0.2),
        "H": (0.5, 0.5),
        "I": (0.1, 0.4),
        "J": (0.1, 0.4),
        "K": (0.1, 0.4),
        "L": (0.1, 0.4),
    }
    for label, (r, c) in label_positions.items():
        x_offset = c * 0.5 + label_shifts.get(label, (0,0))[0]
        y_offset = (5 - r)*height + label_shifts.get(label, (0,0))[1]
        ax.text(x_offset, y_offset, label, color="red", fontsize=16,
                ha="center", va="center")

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
st.title("Hanagramアプリ（初期値セル=薄青、選択セル=黄、他=白）")

#############################################
# 列(A～L), 番号(0～8) => (row,col)
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

col_letter = st.selectbox("列(A～L)", list(lines_map.keys()))
pos_index = st.selectbox("番号(0～8)", list(range(9)))

# 選択されたマスの座標
row, col = lines_map[col_letter][pos_index]

#############################################
# 数字入力UI
#############################################
number = st.selectbox("数字を選んでください", [None,0,1,2,3,4,5,6,7,8,9])

if st.button("数字をセルに入力"):
    # ボード構造を参照
    board_structure = [
        ['N','N','N','U','D','U','N','N','N'],
        ['U','D','U','D','U','D','U','D','U'],
        ['D','U','D','U','D','U','D','U','D'],
        ['U','D','U','D','U','D','U','D','U'],
        ['D','U','D','U','D','U','D','U','D'],
        ['N','N','N','D','U','D','N','N','N'],
    ]
    # 1) セルが存在するか
    if board_structure[row][col] == 'N':
        st.warning("ここはセルが存在しません。")
    else:
        # 2) 初期値かどうか
        if st.session_state.initial_board_values[row][col] is not None:
            st.warning("このセルは初期値なので変更できません。")
        else:
            # 3) 入力を反映
            st.session_state.board_values[row][col] = number

#############################################
# ボード描画
#############################################
draw_board(st.session_state.board_values, (row,col), st.session_state.initial_board_values)

#############################################
# 以下、重複チェックや完成判定・CSV読込等を追加
#############################################

def generate_combinations():
    board_structure = [
        ['N','N','N','U','D','U','N','N','N'],
        ['U','D','U','D','U','D','U','D','U'],
        ['D','U','D','U','D','U','D','U','D'],
        ['U','D','U','D','U','D','U','D','U'],
        ['D','U','D','U','D','U','D','U','D'],
        ['N','N','N','D','U','D','N','N','N'],
    ]
    combos = {
        '横': [],
        '斜め_右上から左下': [],
        '斜め_左上から右下': [],
    }
    # 横方向
    for r_idx, row_data in enumerate(board_structure):
        temp_row = []
        for c_idx, cell in enumerate(row_data):
            if cell != 'N':
                temp_row.append((r_idx, c_idx))
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
    duplicates_found = False
    duplicate_info = []
    for direction, lines in combos.items():
        for idx, line in enumerate(lines):
            nums_in_line = []
            for (r, c) in line:
                val = board_values[r][c]
                if val is not None:
                    nums_in_line.append(val)
            dups = set([num for num in nums_in_line if nums_in_line.count(num) > 1])
            if dups:
                duplicates_found = True
                duplicate_info.append(
                    f"{direction} - 列{idx+1} に重複: {dups}"
                )
    return duplicates_found, duplicate_info

def check_all_lines_completed(board_values, combos):
    # 各ラインの9マスに None が無く、重複なし → 完成とみなす
    for direction, lines in combos.items():
        for line in lines:
            digits = []
            for (r, c) in line:
                val = board_values[r][c]
                if val is None:
                    return False
                digits.append(val)
            if len(set(digits)) != 9:
                return False
    return True

combinations = generate_combinations()

# 重複チェック
duplicates_found, duplicate_info = check_duplicates(st.session_state.board_values, combinations)
st.subheader("重複チェック結果")
if duplicates_found:
    st.error("⚠️ 重複あり")
    for info in duplicate_info:
        st.write(info)
else:
    st.success("✅ 重複はありません")

# 完成判定
if check_all_lines_completed(st.session_state.board_values, combinations):
    st.balloons()
    st.success("🎉 全ライン完成です！")

# CSV読込関数
def load_puzzle_from_csv(filename):
    df = pd.read_csv(filename, header=None)
    arr = df.where(pd.notnull(df), None).values.tolist()
    for r_idx, row_data in enumerate(arr):
        for c_idx, val in enumerate(row_data):
            if val is not None:
                arr[r_idx][c_idx] = int(val)
    return arr

# パズル読込UI
puzzle_folder = "puzzles"
if os.path.isdir(puzzle_folder):
    puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith(".csv")]
    if puzzle_files:
        selected_file = st.selectbox("パズルを選択", puzzle_files)
        if st.button("選択したパズルを読み込み"):
            puzzle_path = os.path.join(puzzle_folder, selected_file)
            loaded_puzzle = load_puzzle_from_csv(puzzle_path)
            st.session_state.board_values = loaded_puzzle
            # 最初に読み込んだ状態だけが初期値
            st.session_state.initial_board_values = loaded_puzzle
            st.success(f"{selected_file} を読み込みました！")
else:
    st.warning("puzzles フォルダが見つかりません。")
