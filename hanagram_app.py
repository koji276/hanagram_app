import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def draw_triangle(ax, x, y, direction='U', value=None):
    height = np.sqrt(3) / 2
    if direction == 'U':
        points = np.array([[x, y], [x + 0.5, y + height], [x + 1, y]])
    else:  # D
        points = np.array([[x, y + height], [x + 0.5, y], [x + 1, y + height]])

    polygon = plt.Polygon(points, edgecolor='black', fill=None)
    ax.add_patch(polygon)

    if value is not None:
        cx = x + 0.5
        cy = y + height / 2
        ax.text(cx, cy, str(value), fontsize=14, ha='center', va='center')

def draw_board_with_numbers(board_values):
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
                cell_value = board_values[row_idx][col_idx]
                draw_triangle(ax, x_offset, y_offset, direction=cell, value=cell_value)

    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Streamlit対応に変更
    st.pyplot(fig)

# Streamlitのページ設定
st.title('Hanagramアプリ（Streamlit版）')

# ボードに配置する数字 (例としてNone)
board_values = [
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, N
