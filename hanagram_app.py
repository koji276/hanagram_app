import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def draw_triangle(ax, x, y, direction='U', value=None, color='white'):
    height = np.sqrt(3) / 2
    if direction == 'U':
        points = np.array([[x, y],
                           [x + 0.5, y + height],
                           [x + 1, y]])
    else:
        points = np.array([[x, y + height],
                           [x + 0.5, y],
                           [x + 1, y + height]])

    polygon = plt.Polygon(points, edgecolor='black', facecolor=color)
    ax.add_patch(polygon)

    if value is not None:
        cx = x + 0.5
        cy = y + height / 2
        ax.text(cx, cy, str(value), fontsize=14, ha='center', va='center')

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

    # --- 三角形マスの描画 ---
    for r_idx, row_data in enumerate(board_structure):
        for c_idx, cell in enumerate(row_data):
            if cell != 'N':
                x_offset = c_idx * 0.5
                y_offset = (5 - r_idx) * height
                value = board_values[r_idx][c_idx]

                # 色分けロジック
                if initial_board_values[r_idx][c_idx] is not None:
                    color = 'yellow'
                elif selected_pos == (r_idx, c_idx):
                    color = 'lightblue'
                else:
                    color = 'white'

                draw_triangle(ax, x_offset, y_offset, direction=cell,
                              value=value, color=color)

    # --- ラベルを配置する ---
    #   各ラベルの(行,列)位置はユーザ定義
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

    # A～D だけ上・右に少しずらす(例)
    label_shifts = {
        "A": (0.2, 0.2),
        "B": (0.2, 0.2),
        "C": (0.2, 0.2),
        "D": (0.2, 0.2),
        # ほかのラベルは(0,0)で表示
    }

    for label, (r, c) in label_positions.items():
        # 同じ座標変換を使う
        x_offset = c * 0.5
        y_offset = (5 - r) * height

        # ラベルごとの微調整
        dx, dy = label_shifts.get(label, (0, 0))
        x_offset += dx
        y_offset += dy

        ax.text(x_offset, y_offset, label, color="red", fontsize=16,
                ha="center", va="center")

    # 表示範囲を広めに
    ax.set_xlim(-2, 7)
    ax.set_ylim(-2, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)


# 以下はパズル全体の処理・UI (例)

if 'board_values' not in st.session_state:
    st.session_state.board_values = [[None]*9 for _ in range(6)]

if 'initial_board_values' not in st.session_state:
    st.session_state.initial_board_values = [[None]*9 for _ in range(6)]

st.title('Hanagramアプリ（ラベル位置を微調整）')

# 列(A~L)＆番号(0~8) 選択
lines_map = {
    "A": [(0, 4), (0, 3), (1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (4, 0)],
    "B": [(0, 5), (1, 5), (1, 4), (2, 4), (2, 3), (3, 3), (3, 2), (4, 2), (4, 1)],
    "C": [(1, 7), (1, 6), (2, 6), (2, 5), (3, 5), (3, 4), (4, 4), (4, 3), (5, 3)],
    "D": [(1, 8), (2, 8), (2, 7), (3, 7), (3, 6), (4, 6), (4, 5), (5, 5), (5, 4)],
    "E": [(4, 8), (3, 8), (3, 7), (2, 7), (2, 6), (1, 6), (1, 5), (0, 5), (0, 4)],
    "F": [(4, 7), (4, 6), (3, 6), (3, 5), (2, 5), (2, 4), (1, 4), (1, 3), (0, 3)],
    "G": [(5, 5), (4, 5), (4, 4), (3, 4), (3, 3), (2, 3), (2, 2), (1, 2), (1, 1)],
    "H": [(5, 4), (5, 3), (4, 3), (4, 2), (3, 2), (3, 1), (2, 1), (2, 0), (1, 0)],
    "I": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)],
    "J": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)],
    "K": [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
    "L": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)]
}

col_letter = st.selectbox("列(A〜L)", list(lines_map.keys()))
pos_index = st.selectbox("番号(0〜8)", list(range(9)))
(row, col) = lines_map[col_letter][pos_index]

# 入力数字
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
        if st.session_state.initial_board_values[row][col] is not None:
            st.warning('このセルは初期値なので変更できません。')
        else:
            st.session_state.board_values[row][col] = number

draw_board(st.session_state.board_values, (row, col), st.session_state.initial_board_values)

# 完成チェック
if all(None not in row_vals for row_vals in st.session_state.board_values):
    st.balloons()
    st.success("🎉 おめでとうございます！完成です！")


###############################################################################
# あとは重複チェックやCSV読み込みなど従来通り
###############################################################################
