import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class PortalMaze3D:
    def __init__(self, width, height, depth, vertical_prob=0.15):
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.depth = depth
        self.vertical_prob = vertical_prob 
        
        # 初始化 3D 迷宮
        self.maze = [[[1 for _ in range(self.width)] 
                      for _ in range(self.height)] 
                     for _ in range(self.depth)]
        
        # 初始化每層的計數器 (Layer 0->A, Layer 1->B...)
        # 用來記錄每一組層級關係產生了多少個傳送門
        self.layer_counters = [0] * self.depth

    def _get_portal_tag(self, lower_layer_idx):
        """
        生成標籤：
        lower_layer_idx = 0 -> 返回 "A1", "A2"... (代表連接 L1-L2)
        lower_layer_idx = 1 -> 返回 "B1", "B2"... (代表連接 L2-L3)
        """
        # 轉換數字為字母: 0->A, 1->B, 2->C
        char_code = chr(ord('A') + lower_layer_idx)
        
        # 該層計數器 +1
        self.layer_counters[lower_layer_idx] += 1
        count = self.layer_counters[lower_layer_idx]
        
        return f"{char_code}{count}"

    def generate(self):
        start_x, start_y, start_z = 1, 1, 0
        print(f"生成結構: {self.width}x{self.height}x{self.depth}")
        
        self.maze[start_z][start_y][start_x] = 0
        self._carve(start_x, start_y, start_z)
        
        # 設定出入口
        self.maze[0][1][0] = 'IN'
        
        # 尋找最後一層的出口
        found_exit = False
        for y in range(self.height-2, 0, -1):
            for x in range(self.width-2, 0, -1):
                if self.maze[self.depth-1][y][x] == 0:
                    self.maze[self.depth-1][y][x] = 'OUT'
                    found_exit = True
                    break
            if found_exit: break
            
        print("生成完畢，標籤已統一。")

    def _carve(self, cx, cy, cz):
        # 定義移動：水平(步長2)、垂直(步長1)
        moves = [
            ('H', 0, 1, 0), ('H', 0, -1, 0), 
            ('H', 1, 0, 0), ('H', -1, 0, 0),
            ('V', 0, 0, 1), ('V', 0, 0, -1)
        ]
        random.shuffle(moves)

        for mode, dx, dy, dz in moves:
            if mode == 'H':
                nx, ny, nz = cx + dx * 2, cy + dy * 2, cz
                if (0 <= nx < self.width and 0 <= ny < self.height):
                    if self.maze[nz][ny][nx] == 1:
                        self.maze[cz][cy + dy][cx + dx] = 0
                        self.maze[nz][ny][nx] = 0
                        self._carve(nx, ny, nz)
            
            elif mode == 'V':
                if random.random() > self.vertical_prob:
                    continue

                nx, ny, nz = cx, cy, cz + dz # 垂直直接堆疊
                
                if (0 <= nz < self.depth):
                    if self.maze[nz][ny][nx] == 1:
                        # --- 核心修改邏輯 ---
                        
                        # 1. 判斷誰是「底層」 (用來決定是 A系列還是 B系列)
                        lower_layer = min(cz, nz)
                        
                        # 2. 獲取唯一的標籤 (例如 "A5")
                        tag = self._get_portal_tag(lower_layer)
                        
                        # 3. 將上下兩層的對應點都設為同一個標籤
                        self.maze[cz][cy][cx] = tag
                        self.maze[nz][ny][nx] = tag
                        
                        self._carve(nx, ny, nz)

    def _get_color(self, tag_str):
        """根據標籤的首字母決定顏色，方便視覺區分"""
        if tag_str == 'IN': return '#32CD32', 'white' # 綠色
        if tag_str == 'OUT': return '#DC143C', 'white' # 紅色
        
        # 依據字母變色
        first_char = tag_str[0]
        if first_char == 'A': return '#1E90FF', 'white' # 藍色系 (L1-L2)
        if first_char == 'B': return '#FF8C00', 'black' # 橘色系 (L2-L3)
        if first_char == 'C': return '#9370DB', 'white' # 紫色系 (L3-L4)
        
        return 'gray', 'white'

    def draw(self):
        cols = self.depth
        fig, axes = plt.subplots(1, cols, figsize=(5 * cols, 6))
        if self.depth == 1: axes = [axes]

        for z in range(self.depth):
            ax = axes[z]
            ax.set_title(f"Level {z+1}", fontsize=16, fontweight='bold', pad=12)
            
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.maze[z][y][x]
                    
                    if cell == 1: # 牆
                        rect = patches.Rectangle((x, self.height - 1 - y), 1, 1, facecolor='black')
                        ax.add_patch(rect)
                    elif cell == 0: # 路
                        pass # 預設留白
                    else: # 標籤 (A1, B2, IN, OUT)
                        bg, fg = self._get_color(cell)
                        rect = patches.Rectangle((x, self.height - 1 - y), 1, 1, facecolor=bg)
                        ax.add_patch(rect)
                        ax.text(x + 0.5, self.height - 1 - y + 0.5, cell, 
                                ha='center', va='center', color=fg, 
                                fontsize=9, fontweight='bold')

            # 網格線輔助
            ax.set_xticks(range(self.width + 1))
            ax.set_yticks(range(self.height + 1))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(color='lightgray', linestyle='-', linewidth=0.5, alpha=0.3)
            
            ax.set_xlim(0, self.width)
            ax.set_ylim(0, self.height)
            ax.set_aspect('equal')

        plt.tight_layout()
        plt.show()

# --- 執行 ---
if __name__ == "__main__":
    WIDTH = 15
    HEIGHT = 15
    DEPTH = 5
    V_PROB = 0.2

    gen = PortalMaze3D(WIDTH, HEIGHT, DEPTH, V_PROB)
    gen.generate()
    gen.draw()