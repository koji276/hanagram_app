import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# --- 三角形描画関数 ---
def draw_triangle(ax, x, y, direction='U', value=None, color='white'):
    height = np.sqrt(3) / 2
    if direction == 'U':
        points = np.array([[x, y], [x + 0.5, y + height], [x + 1, y]])
    else:
        points = np.array([[x, y + height], [x + 0.5, y], [x + 1, y + height]])

    polygon = plt.Polygon(points, edgecolor='black', facecolor=color)
    ax.add_patch(polygon)

    if value is not None:
        cx = x + 0.5
        cy = y + height / 2
        ax.text(cx, cy, str(value), fontsize=14, ha='center', va='center')


# --- ボード描画関数 ---
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
    for row_idx, row_data in enumerate(board_structure):
        for col_idx, cell in enumerate(row_data):
            if cell != 'N':
                x_offset = col_idx * 0.5
                # row_idx=0が上部なので、下に行くほどy_offsetを小さくする
                y_offset = (5 - row_idx) * height
                value = board_values[row_idx][col_idx]

                # 色分けロジック
                if initial_board_values[row_idx][col_idx] is not None:
                    color = 'yellow'       # 初期値のセル
                elif selected_pos == (row_idx, col_idx):
                    color = 'lightblue'   # 選択中のセル
                else:
                    color = 'white'       # 通常セル

                draw_triangle(ax, x_offset, y_offset,
                              direction=cell, value=value, color=color)

    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)


# --- セッション初期化 ---
if 'board_values' not in st.session_state:
    st.session_state.board_values = [[None]*9 for _ in range(6)]

# 初期値用の配列をセッションに持たせる
if 'initial_board_values' not in st.session_state:
    st.session_state.initial_board_values = [[None]*9 for _ in range(6)]


st.title('Hanagramアプリ（インタラクティブ版）')


###############################################################################
# ここから「列(A～L) ＋ 番号(0～8)」によるマッピングを導入
###############################################################################
lines_map = {
    # 上記で示された各「列(A～L)」に紐づく9マスの座標
    "A": [(0, 4), (0, 5), (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8)],
    "B": [(0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7)],
    "C": [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)],
    "D": [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 3), (5, 4)],

    "E": [(4, 8), (3, 8), (3, 7), (2, 7), (2, 6), (1, 6), (1, 5), (0, 5), (0, 4)],
    "F": [(4, 7), (4, 6), (3, 6), (3, 5), (2, 5), (2, 4), (1, 4), (1, 3), (0, 3)],
    "G": [(5, 5), (4, 5), (4, 4), (3, 4), (3, 3), (2, 3), (2, 2), (1, 2), (1, 1)],
    "H": [(5, 4), (5, 3), (4, 3), (4, 2), (3, 2), (3, 1), (2, 1), (2, 0), (1, 0)],

    "I": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)],
    "J": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)],
    "K": [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
    "L": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)]
}

# 列(A~L) 選択
col_letter = st.selectbox("列(A〜L)", list(lines_map.keys()))

# 番号(0~8) 選択
pos_index = st.selectbox("番号(0〜8)", list(range(9)))

# 上記選択から実際の row,col を取得
row, col = lines_map[col_letter][pos_index]


###############################################################################
# 従来どおり「数字を選択」して入力するUI
###############################################################################
number = st.selectbox("数字を選んでください", [None,0,1,2,3,4,5,6,7,8,9])

if st.button('数字をセルに入力'):
    board_structure = [
        ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
    ]

    # 1) ボード上にセルがあるか確認 (念のため)
    if board_structure[row][col] == 'N':
        st.warning('ここはセルが存在しません。')
    else:
        # 2) 初期値セル(=黄色)の場合は上書き不可
        if st.session_state.initial_board_values[row][col] is not None:
            st.warning('このセルは初期値なので変更できません。')
        else:
            # 3) 入力を受け付ける
            st.session_state.board_values[row][col] = number

# 選択されたセル座標
selected_pos = (row, col)

# ボード描画
draw_board(st.session_state.board_values, selected_pos, st.session_state.initial_board_values)


###############################################################################
# パズル完成チェック
###############################################################################
if all(None not in row_vals for row_vals in st.session_state.board_values):
    st.balloons()
    st.success("🎉 おめでとうございます！完成です！")


###############################################################################
# 以下、重複チェックやCSV読み込みなどの機能は従来どおり
###############################################################################
def generate_combinations():
    board_structure = [
        ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
    ]

    combinations = {
        '横': [],
        '斜め_右上から左下': [],
        '斜め_左上から右下': [],
    }

    # 横方向 (3つ以下を除外)
    for r_idx, row_data in enumerate(board_structure):
        temp_row = []
        for c_idx, cell in enumerate(row_data):
            if cell != 'N':
                temp_row.append((r_idx, c_idx))
        if len(temp_row) > 3:
            combinations['横'].append(temp_row)

    # 斜め方向（右上から左下）
    combinations['斜め_右上から左下'] = [
        [(0, 4), (0, 3), (1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (4, 0)],
        [(0, 5), (1, 5), (1, 4), (2, 4), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1)],
        [(1, 7), (1, 6), (2, 6), (2, 5), (3, 5), (3, 4), (4, 4), (4, 3), (5, 3)],
        [(1, 8), (2, 8), (2, 7), (3, 7), (3, 6), (4, 6), (4, 5), (5, 5), (5, 4)]
    ]

    # 斜め方向（左上から右下）
    combinations['斜め_左上から右下'] = [
        [(0, 4), (0, 5), (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8)],
        [(0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7)],
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)],
        [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 3), (5, 4)]
    ]

    return combinations

def check_duplicates(board_values, combinations):
    duplicates_found = False
    duplicate_info = []

    for direction, lines in combinations.items():
        for idx, line in enumerate(lines):
            nums_in_line = []
            for (r, c) in line:
                value = board_values[r][c]
                if value is not None:
                    nums_in_line.append(value)

            duplicates = set([num for num in nums_in_line if nums_in_line.count(num) > 1])
            if duplicates:
                duplicates_found = True
                duplicate_info.append(
                    f"{direction} - 列{idx+1} で数字が重複しています: {duplicates}"
                )

    return duplicates_found, duplicate_info

combinations = generate_combinations()
st.subheader("12列の組み合わせ確認（テスト表示）")
for direction, lines in combinations.items():
    st.write(f"### {direction}")
    for idx, line in enumerate(lines):
        st.write(f"{direction} - 列{idx+1}: {line}")

st.subheader("🔎 数字の重複チェック結果")
current_board_values = st.session_state.board_values
duplicates_found, duplicate_info = check_duplicates(current_board_values, combinations)

if duplicates_found:
    st.error("⚠️ 重複が見つかりました！以下を確認してください。")
    for info in duplicate_info:
        st.write(info)
else:
    st.success("✅ 現在、重複はありません。")


# --- CSV読込用関数 ---
def load_puzzle_from_csv(filename):
    df = pd.read_csv(filename, header=None)
    board_values = df.where(pd.notnull(df), None).values.tolist()
    
    for r_idx, row_data in enumerate(board_values):
        for c_idx, val in enumerate(row_data):
            if pd.notnull(val):
                board_values[r_idx][c_idx] = int(val)
            else:
                board_values[r_idx][c_idx] = None
    return board_values


puzzle_folder = 'puzzles'
puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith('.csv')]
selected_puzzle_file = st.selectbox('🔍 パズルを選択', puzzle_files)

if st.button('選択したパズルを読み込み'):
    puzzle_path = os.path.join(puzzle_folder, selected_puzzle_file)
    loaded_puzzle = load_puzzle_from_csv(puzzle_path)

    # ロードしたパズルを board_values に設定
    st.session_state.board_values = loaded_puzzle

    # 初期値配列にも同じデータを設定（黄色表示＆入力不可にするため）
    st.session_state.initial_board_values = loaded_puzzle

    st.success(f"{selected_puzzle_file} を読み込みました！")
    # st.experimental_rerun()  # 必要に応じて使用

