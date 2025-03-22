import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# 三角形描画関数
def draw_triangle(ax, x, y, direction='U', value=None, color='white'):
    height = np.sqrt(3) / 2
    points = np.array([[x, y], [x + 0.5, y + height], [x + 1, y]]) if direction == 'U' else \
             np.array([[x, y + height], [x + 0.5, y], [x + 1, y + height]])

    polygon = plt.Polygon(points, edgecolor='black', facecolor=color)
    ax.add_patch(polygon)

    if value is not None:
        cx, cy = x + 0.5, y + height / 2
        ax.text(cx, cy, str(value), fontsize=14, ha='center', va='center')

# ボード描画関数（黄色セル対応）
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
                if initial_board_values[row_idx][col_idx] is not None:
                    color = 'yellow'
                elif selected_pos == (row_idx, col_idx):
                    color = 'lightblue'
                else:
                    color = 'white'
                draw_triangle(ax, x_offset, y_offset, cell, value, color)

    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig)

# セッション初期化
if 'board_values' not in st.session_state:
    st.session_state.board_values = [[None]*9 for _ in range(6)]
if 'initial_board_values' not in st.session_state:
    st.session_state.initial_board_values = [[None]*9 for _ in range(6)]

st.title('Hanagramアプリ（インタラクティブ版）')

# 行列選択
row = st.selectbox("行を選んでください（上から0〜5）", [0,1,2,3,4,5])
col = st.selectbox("列を選んでください（左から0〜8）", [0,1,2,3,4,5,6,7,8])
number = st.selectbox("数字を選んでください", [None,0,1,2,3,4,5,6,7,8,9])

# セルへの数字入力（上書き防止）
if st.button('数字をセルに入力'):
    board_structure = [
        ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
        ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
        ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
    ]
    if board_structure[row][col] != 'N' and st.session_state.initial_board_values[row][col] is None:
        st.session_state.board_values[row][col] = number
    elif st.session_state.initial_board_values[row][col] is not None:
        st.warning('このセルは初期値なので変更できません。')
    else:
        st.warning('ここはセルが存在しません。')

selected_pos = (row, col)
draw_board(st.session_state.board_values, selected_pos, st.session_state.initial_board_values)

# パズル完了チェック
if all(None not in row for row in st.session_state.board_values):
    st.balloons()
    st.success('🎉 おめでとうございます！完成です！')

# puzzlesフォルダからCSV読み込み
def load_puzzle_from_csv(filename):
    df = pd.read_csv(filename, header=None)
    return [[int(val) if pd.notnull(val) else None for val in row] for row in df.values]

puzzle_folder = 'puzzles'
puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith('.csv')]
selected_puzzle_file = st.selectbox('🔍 パズルを選択', puzzle_files)

# パズル読み込み（初期値保存）
if st.button('選択したパズルを読み込み'):
    puzzle_path = os.path.join(puzzle_folder, selected_puzzle_file)
    loaded_puzzle = load_puzzle_from_csv(puzzle_path)
    st.session_state.board_values = loaded_puzzle
    st.session_state.initial_board_values = loaded_puzzle
    st.success(f"{selected_puzzle_file} を読み込みました！")
