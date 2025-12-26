import matplotlib.pyplot as plt
import random

class MazeGenerator:
    def __init__(self, width, height):
        # 為了保證迷宮結構（牆-路-牆），長寬必須是奇數
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        
        # 初始化迷宮：1 代表牆壁，0 代表路徑
        # 先將所有地方填滿牆壁
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

    def generate(self, start_x=1, start_y=1):
        """開始生成迷宮"""
        self.maze[start_y][start_x] = 0  # 設定起點為路徑
        self._carve_passages(start_x, start_y)
        
        # 設定入口和出口
        self.maze[1][0] = 0             # 左上入口
        self.maze[self.height - 2][self.width - 1] = 0  # 右下出口

    def _carve_passages(self, cx, cy):
        """遞迴挖掘路徑"""
        # 定義四個方向 (dx, dy)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)  # 隨機打亂方向

        for dx, dy in directions:
            # nx, ny 是「隔壁的隔壁」的座標 (跨過一面牆)
            nx, ny = cx + dx * 2, cy + dy * 2

            # 檢查邊界，且確保目標點是牆壁（未被訪問過）
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 1:
                # 1. 把中間那道牆打通
                self.maze[cy + dy][cx + dx] = 0
                # 2. 把目標點變成路徑
                self.maze[ny][nx] = 0
                # 3. 遞迴：從新點繼續挖掘
                self._carve_passages(nx, ny)

    def draw(self):
        """使用 Matplotlib 繪製迷宮"""
        plt.figure(figsize=(10, 10))
        plt.imshow(self.maze, cmap='binary') # binary: 黑白配色
        
        # 移除座標軸刻度，讓圖更乾淨
        plt.xticks([])
        plt.yticks([])
        plt.title(f"Random Maze ({self.width}x{self.height})", fontsize=15)
        plt.show()

# --- 主程式 ---
if __name__ == "__main__":
    # 設定迷宮大小 (建議使用奇數，例如 51, 81 等)
    WIDTH = 51
    HEIGHT = 51

    print(f"正在生成 {WIDTH}x{HEIGHT} 的迷宮...")
    generator = MazeGenerator(WIDTH, HEIGHT)
    generator.generate()
    print("生成完畢，正在繪圖...")
    generator.draw()