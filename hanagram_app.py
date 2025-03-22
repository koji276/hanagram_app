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
    for row_idx, row in enumerate(board_structure):
        for col_idx, cell in enumerate(row):
            if cell != 'N':
                x_offset = col_idx * 0.5
                y_offset = (5 - row_idx) * height
                value = board_values[row_idx][col_idx]

                # --- 色分けロジック ---
                if initial_board_values[row_idx][col_idx] is not None:
                    # パズルの初期値があるセルは黄色
                    color = 'yellow'
                elif selected_pos == (row_idx, col_idx):
                    # 選択中のセルは水色
                    color = 'lightblue'
                else:
                    # それ以外は白
                    color = 'white'

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

# 追加：初期値用の配列をセッションに持たせる
if 'initial_board_values' not in st.session_state:
    st.session_state.initial_board_values = [[None]*9 for _ in range(6)]


st.title('Hanagramアプリ（インタラクティブ版）')

# 行・列選択
row = st.selectbox("行を選んでください（上から0〜5）", [0,1,2,3,4,5])
col = st.selectbox("列を選んでください（左から0〜8）", [0,1,2,3,4,5,6,7,8])

# 入力数字選択
number = st.selectbox("数字を選んでください", [None,0,1,2,3,4,5,6,7,8,9])

# --- セルに数字を入力（ボタン） ---
if st.button('数字をセルに入力'):
    board_structure = [
        ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
    ]

    # ① ボード上にセルがあるかを確認
    if board_structure[row][col] == 'N':
        st.warning('ここはセルが存在しません。')
    else:
        # ② 初期値セル(=黄色)の場合は入力不可
        if st.session_state.initial_board_values[row][col] is not None:
            st.warning('このセルは初期値なので変更できません。')
        else:
            # ③ 通常セルなので入力を受け付ける
            st.session_state.board_values[row][col] = number


selected_pos = (row, col)
draw_board(st.session_state.board_values, selected_pos,
           st.session_state.initial_board_values)


# --- セル位置を基準に12列を生成する関数 ---
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
    for row_idx, row in enumerate(board_structure):
        temp_row = []
        for col_idx, cell in enumerate(row):
            if cell != 'N':
                temp_row.append((row_idx, col_idx))
        if len(temp_row) > 3:
            combinations['横'].append(temp_row)

    # 斜め方向（右上から左下）【手動定義済み】
    combinations['斜め_右上から左下'] = [
        [(0, 4), (0, 3), (1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (4, 0)],
        [(0, 5), (1, 5), (1, 4), (2, 4), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1)],
        [(1, 7), (1, 6), (2, 6), (2, 5), (3, 5), (3, 4), (4, 4), (4, 3), (5, 3)],
        [(1, 8), (2, 8), (2, 7), (3, 7), (3, 6), (4, 6), (4, 5), (5, 5), (5, 4)]
    ]

    # 斜め方向（左上から右下）【手動定義】
    combinations['斜め_左上から右下'] = [
        [(0, 4), (0, 5), (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8)],
        [(0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7)],
        [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)],
        [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 3), (5, 4)]
    ]

    return combinations


# --- 重複チェック関数 ---
def check_duplicates(board_values, combinations):
    duplicates_found = False
    duplicate_info = []

    for direction, lines in combinations.items():
        for idx, line in enumerate(lines):
            nums_in_line = []
            for r, c in line:
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


# --- 12列の組み合わせ作成＆テスト表示 ---
combinations = generate_combinations()
st.subheader("12列の組み合わせ確認（テスト表示）")
for direction, lines in combinations.items():
    st.write(f"### {direction}")
    for idx, line in enumerate(lines):
        st.write(f"{direction} - 列{idx+1}: {line}")


# --- 重複チェック結果を表示 ---
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
    
    for r_idx, row in enumerate(board_values):
        for c_idx, val in enumerate(row):
            if pd.notnull(val):
                board_values[r_idx][c_idx] = int(val)
            else:
                board_values[r_idx][c_idx] = None
    return board_values


# --- パズルファイル選択と読み込み ---
puzzle_folder = 'puzzles'
puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith('.csv')]
selected_puzzle_file = st.selectbox('🔍 パズルを選択', puzzle_files)

if st.button('選択したパズルを読み込み'):
    puzzle_path = os.path.join(puzzle_folder, selected_puzzle_file)
    loaded_puzzle = load_puzzle_from_csv(puzzle_path)

    # ロードしたパズルを board_values に設定
    st.session_state.board_values = loaded_puzzle

    # 「初期値配列」にも同じものを設定（黄色表示＆入力不可にするため）
    st.session_state.initial_board_values = loaded_puzzle

    st.success(f"{selected_puzzle_file} を読み込みました！")
    # 読み込み後は描画を更新
    # st.experimental_rerun()  # 必要に応じてコメント解除すると即再描画リロード
