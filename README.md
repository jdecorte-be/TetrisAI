
<h1 align="center">
    📖 Tetris AI: The Art of Perfect Play
</h1>

<p align="center">
    <b><i>Mastering the Classic Game with Advanced AI</i></b><br>
</p>

<p align="center">
    <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/jdecorte-be/TetrisAI?color=lightblue" />
    <img alt="Number of lines of code" src="https://img.shields.io/tokei/lines/github/jdecorte-be/TetrisAI?color=critical" />
    <img alt="Code language count" src="https://img.shields.io/github/languages/count/jdecorte-be/TetrisAI?color=yellow" />
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/jdecorte-be/TetrisAI?color=blue" />
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/jdecorte-be/TetrisAI?color=green" />
</p>

Dive into the world of Tetris AI, where advanced algorithms and strategic computations redefine how we play and master one of the most iconic video games. The essence of Tetris AI is to not just play Tetris, but to master it with precision, strategy, and computational intelligence.

## Installation

Ensure you have Python 3 installed on your system.

Clone the Tetris AI repository:
```bash
git clone https://github.com/jdecorte-be/TetrisAI.git
cd TetrisAI
```

## Learning and Testing

To train the AI model, run:
```bash
python3 learn.py
```

For testing the AI's performance, execute:
```bash
python3 test.py
```

### The Objective of Tetris AI

The primary goal of Tetris AI is not just to play Tetris but to excel at it. This involves mastering the game mechanics and employing strategies to maximize the score while minimizing the risk of losing.

### How Does Tetris AI Work?

The AI employs various strategies and algorithms to optimize piece placement. It analyzes the board's current state, upcoming pieces, and potential future challenges, striving to avoid game-ending scenarios and maintain a clear board.

### Aggregate Height
![home](https://codemyroad.files.wordpress.com/2013/04/121.png)
Aggregate height is a crucial factor in Tetris AI. It measures the cumulative height of all the columns on the board. The AI aims to keep this value as low as possible to minimize the risk of topping out.

### Complete Lines
![login](https://codemyroad.files.wordpress.com/2013/04/2.png)
Complete lines are the essence of scoring in Tetris. The AI focuses on clearing multiple lines simultaneously, known as 'Tetrises', for maximum scoring efficiency. This involves strategically placing pieces to enable line clears while avoiding pile-ups.

### Holes
![chat](https://codemyroad.files.wordpress.com/2013/04/3.png)
Holes are empty spaces blocked from above by Tetriminos. The AI aims to minimize holes as they complicate future placements and hinder line completion. The strategy involves filling gaps and preventing new holes from forming.

### Bumpiness
![add](https://codemyroad.files.wordpress.com/2013/04/4.png)
Bumpiness refers to the roughness of the surface of the Tetris playfield. High bumpiness means more uneven surfaces and gaps. The AI seeks to keep the playfield as even as possible, reducing bumpiness to make piece placement easier and more predictable.

### Challenges in Creating Tetris AI
Developing an AI capable of playing Tetris near-perfectly involves overcoming challenges like rapid decision-making and adaptability to evolving board states, all while maintaining calculation efficiency to keep pace with the game.

### Conclusion

Creating a near-perfect Tetris player is a complex yet fascinating endeavor, showcasing how AI can master and optimize gameplay in a classic game like Tetris. This mirrors the broader advancements in AI, highlighting its growing ability to tackle and excel in human-designed challenges.

