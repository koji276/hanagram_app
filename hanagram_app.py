import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 三角形を描画する関数（正三角形）
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

# ボード描画関数
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

if st.button('数字をセルに入力
