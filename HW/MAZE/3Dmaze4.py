import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class ExcelStyleMaze:
    def __init__(self, width, height, depth, vertical_prob=0.15):
        # 確保寬高為奇數以配合迷宮算法
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.depth = depth
        self.vertical_prob = vertical_prob
        
        # 初始化迷宮：1=牆, 0=路
        self.maze = [[[1 for _ in range(self.width)] 
                      for _ in range(self.height)] 
                     for _ in range(self.depth)]
        
        # 每層獨立的計數器 (Layer 0->A, Layer 1->B...)
        self.layer_counters = [0] * self.depth

    def _get_portal_tag(self, layer1, layer2):
        """
        生成標籤：
        1. 找出較低的樓層作為「主色調/字母」來源
        2. 取出流水號
        """
        base_layer = min(layer1, layer2)
        
        # 轉換為字母: 0->A, 1->B, 2->C...
        letter = chr(ord('A') + base_layer)
        
        # 計數器 +1
        self.layer_counters[base_layer] += 1
        num = self.layer_counters[base_layer]
        
        return f"{letter}{num}"

    def generate(self):
        # 設定起始點
        start_x, start_y, start_z = 1, 1, 0
        print(f"生成迷宮: {self.width}x{self.height}x{self.depth}")
        print("模式: 生長樹演算法 (混合長路徑與多分支)")
        
        # 設定入口
        self.maze[0][1][0] = 'IN'
        self.maze[start_z][start_y][start_x] = 0
        
        # --- 使用迭代式生長樹演算法取代遞迴 ---
        # active_cells 存放 (x, y, z)
        active_cells = [(start_x, start_y, start_z)]
        
        while active_cells:
            # === 關鍵修改點 ===
            # 決定從列表中選取哪一個格子來延伸
            # 讓 random.random() < 0.5 決定：
            # True: 選最後一個 (模擬遞迴，產生長路徑)
            # False: 隨機選一個 (模擬 Prim 演算法，產生多分支)
            if random.random() < 0.5:
                index = -1 
            else:
                index = random.randint(0, len(active_cells) - 1)
            
            cx, cy, cz = active_cells[index]
            
            # 尋找所有可能的鄰居 (水平 + 垂直)
            moves = [('H', 0, 1), ('H', 0, -1), ('H', 1, 0), ('H', -1, 0), ('V', 0, 0)]
            random.shuffle(moves)
            
            found_neighbor = False
            
            for mode, dx, dy in moves:
                if mode == 'H':
                    nx, ny, nz = cx + dx * 2, cy + dy * 2, cz
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.maze[nz][ny][nx] == 1:
                            # 打通牆壁
                            self.maze[cz][cy + dy][cx + dx] = 0
                            self.maze[nz][ny][nx] = 0
                            # 加入列表
                            active_cells.append((nx, ny, nz))
                            found_neighbor = True
                            break # 找到一個就跳出，換下一個迴圈處理
                            
                elif mode == 'V':
                    # 垂直跳躍邏輯
                    if random.random() > self.vertical_prob:
                        continue
                        
                    # 尋找其他樓層作為目標
                    candidates = list(range(self.depth))
                    candidates.remove(cz)
                    random.shuffle(candidates)
                    
                    for target_z in candidates:
                        # 只有當目標點是牆壁(未訪問)時才跳躍
                        if self.maze[target_z][cy][cx] == 1:
                            tag = self._get_portal_tag(cz, target_z)
                            
                            # 標記
                            self.maze[cz][cy][cx] = tag
                            self.maze[target_z][cy][cx] = tag
                            
                            # 加入列表
                            active_cells.append((cx, cy, target_z))
                            found_neighbor = True
                            break
                    
                    if found_neighbor:
                        break

            # 如果這個格子四周都已經沒有可以挖掘的地方，就從列表中移除
            if not found_neighbor:
                active_cells.pop(index)

        # 生成結束後設定出口
        self._set_exit()

    def _set_exit(self):
        # 設定出口 (在最底層找路徑點)
        found = False
        for y in range(self.height-2, 0, -1):
            for x in range(self.width-2, 0, -1):
                if self.maze[self.depth-1][y][x] == 0:
                    self.maze[self.depth-1][y][x] = 'OUT'
                    found = True
                    break
            if found: break
  
    def _get_style(self, tag):
        """
        根據您的圖片風格設定顏色：
        A -> 紅色
        B -> 黃色/橘黃
        C -> 綠色
        D -> 肉色/淡橘
        E -> 紫色/粉色
        """
        if tag == 'IN': return '#32CD32', 'white' # 鮮綠
        if tag == 'OUT': return '#FF0000', 'white' # 紅
        
        letter = tag[0]
        
        # 參考圖片的配色方案
        colors = {
            'A': ('#FF0000', 'white'), # 紅底白字
            'B': ('#FFC125', 'black'), # 金黃底黑字
            'C': ('#00FF7F', 'black'), # 春綠底黑字
            'D': ('#FFDAB9', 'black'), # 桃色底黑字 (PeachPuff) 或近似肉色
            'E': ('#DA70D6', 'white'), # 蘭花紫 (Orchid)
            'F': ('#1E90FF', 'white'), # 藍色
        }
        
        # 預設灰色
        return colors.get(letter, ('gray', 'white'))

    def draw(self):
        cols = self.depth
        # 調整圖表比例以接近 Excel 表格形狀
        fig, axes = plt.subplots(1, cols, figsize=(6 * cols, 6))
        if self.depth == 1: axes = [axes]

        for z in range(self.depth):
            ax = axes[z]
            layer_char = chr(ord('A') + z)
            ax.set_title(f"Layer {z+1} (Start Code: {layer_char})", fontsize=14, fontweight='bold')
            
            # 繪製背景 (淡藍色，模仿 Excel)
            ax.set_facecolor('#B0C4DE') 

            for y in range(self.height):
                for x in range(self.width):
                    cell = self.maze[z][y][x]
                    
                    # 繪製順序：先畫格子，再畫文字
                    # 注意 Matplotlib 的 Y 軸是下到上，我們需要反轉來符合矩陣
                    rect_y = self.height - 1 - y
                    
                    if cell == 1: # 牆壁 (留白或淡藍色背景)
                        # 這裡我們不畫任何東西，讓背景色透出來，或者畫白色
                        # 根據您的圖片，牆是白色的，路是淡藍色的？
                        # 不，通常迷宮圖中，牆是實心，路是空心。
                        # 讓我們模仿圖片：背景是藍色，路是白色。
                        pass 
                    else:
                        # 路徑或通道
                        # 先畫一個白色底塊代表路徑
                        base_rect = patches.Rectangle((x, rect_y), 1, 1, facecolor='white', edgecolor='lightgray', linewidth=0.5)
                        ax.add_patch(base_rect)

                        if isinstance(cell, str): # 如果是標籤 (A1, B5...)
                            bg, fg = self._get_style(cell)
                            # 畫彩色方塊
                            tag_rect = patches.Rectangle((x + 0.1, rect_y + 0.1), 0.8, 0.8, 
                                                       facecolor=bg, edgecolor=None)
                            ax.add_patch(tag_rect)
                            
                            # 寫字
                            ax.text(x + 0.5, rect_y + 0.5, cell, 
                                    ha='center', va='center', color=fg, 
                                    fontsize=8, fontweight='bold')

            ax.set_xlim(0, self.width)
            ax.set_ylim(0, self.height)
            
            # 模擬 Excel 的 Grid 線
            ax.set_xticks(range(self.width + 1))
            ax.set_yticks(range(self.height + 1))
            ax.grid(color='white', linestyle='-', linewidth=1)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            
            ax.set_aspect('equal')

        plt.tight_layout()
        plt.show()

# --- 執行設定 ---
if __name__ == "__main__":
    # 參數設定
    WIDTH = 25      
    HEIGHT = 25    
    DEPTH = 4       # 設定 4 層
    V_PROB = 0.08    # 垂直跳躍機率

    gen = ExcelStyleMaze(WIDTH, HEIGHT, DEPTH, V_PROB)
    gen.generate()
    gen.draw()