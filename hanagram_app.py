import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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

def draw_board(board_values, selected_pos):
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
                color = 'lightblue' if selected_pos == (row_idx, col_idx) else 'white'
                draw_triangle(ax, x_offset, y_offset, direction=cell, value=value, color=color)

    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# Streamlit セッションの初期化
if 'board_values' not in st.session_state:
    st.session_state.board_values = [[None]*9 for _ in range(6)]

st.title('Hanagramアプリ（インタラクティブ版）')

# 行列選択
row = st.selectbox("行を選んでください（上から0〜5）", [0,1,2,3,4,5])
col = st.selectbox("列を選んでください（左から0〜8）", [0,1,2,3,4,5,6,7,8])

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
    if board_structure[row][col] != 'N':
        st.session_state.board_values[row][col] = number
    else:
        st.warning('ここはセルが存在しません。')

selected_pos = (row, col)
draw_board(st.session_state.board_values, selected_pos)

# セル位置を基準に12列を生成する関数
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

    # 横方向の4列 (上から順に)
    for row_idx, row in enumerate(board_structure):
        temp_row = []
        for col_idx, cell in enumerate(row):
            if cell != 'N':
                temp_row.append((row_idx, col_idx))
        if temp_row:
            combinations['横'].append(temp_row)

    # 斜め方向（右上から左下）
    diagonals_rl = {}
    for row_idx in range(6):
        for col_idx in range(9):
            if board_structure[row_idx][col_idx] != 'N':
                key = col_idx - row_idx
                diagonals_rl.setdefault(key, []).append((row_idx, col_idx))

    combinations['斜め_右上から左下'] = [v for v in diagonals_rl.values() if len(v) > 1]

    # 斜め方向（左上から右下）
    diagonals_lr = {}
    for row_idx in range(6):
        for col_idx in range(9):
            if board_structure[row_idx][col_idx] != 'N':
                key = col_idx + row_idx
                diagonals_lr.setdefault(key, []).append((row_idx, col_idx))

    combinations['斜め_左上から右下'] = [v for v in diagonals_lr.values() if len(v) > 1]

    return combinations

# 組み合わせを表示（テスト用）
combinations = generate_combinations()

# Streamlit上で確認
st.subheader("12列の組み合わせ確認（テスト表示）")
for direction, lines in combinations.items():
    st.write(f"### {direction}")
    for idx, line in enumerate(lines):
        st.write(f"{direction} - 列{idx+1}: {line}")

