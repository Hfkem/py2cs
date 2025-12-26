import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import string

class Maze3DGenerator:
    def __init__(self, width, height, depth):
        # 確保長寬高都是奇數
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.depth = depth if depth % 2 != 0 else depth + 1
        
        # 初始化 3D 迷宮：[z][y][x]
        self.maze = [[[1 for _ in range(self.width)] 
                      for _ in range(self.height)] 
                     for _ in range(self.depth)]
        
        self.tag_letter_idx = 0
        self.tag_number = 1
        self.vertical_tags = {} 

    def _get_next_tag(self):
        """生成下一個垂直通道標籤"""
        letter = string.ascii_uppercase[self.tag_letter_idx]
        tag = f"{letter}{self.tag_number}"
        
        self.tag_letter_idx += 1
        if self.tag_letter_idx >= 26:
            self.tag_letter_idx = 0
            self.tag_number += 1
        return tag

    def generate(self, start_x=1, start_y=1, start_z=0):
        print(f"開始生成 {self.width}x{self.height}x{self.depth} 的 3D 迷宮...")
        self.maze[start_z][start_y][start_x] = 0
        self._carve_passages_3d(start_x, start_y, start_z)
        
        # 設定出入口
        self.maze[0][1][0] = 'IN'  
        self.maze[self.depth - 1][self.height - 2][self.width - 1] = 'OUT'
        print("生成完畢！")

    def _carve_passages_3d(self, cx, cy, cz):
        directions = [
            (0, 1, 0), (0, -1, 0), # 南北
            (1, 0, 0), (-1, 0, 0), # 東西
            (0, 0, 1), (0, 0, -1)  # 上下
        ]
        random.shuffle(directions)

        for dx, dy, dz in directions:
            nx, ny, nz = cx + dx * 2, cy + dy * 2, cz + dz * 2

            if (0 <= nx < self.width and 
                0 <= ny < self.height and 
                0 <= nz < self.depth):
                
                if self.maze[nz][ny][nx] == 1:
                    
                    if dz != 0: 
                        # --- 垂直移動 ---
                        tag = self._get_next_tag()
                        self.maze[cz][cy][cx] = tag
                        self.maze[cz + dz][cy + dy][cx + dx] = tag
                        self.maze[nz][ny][nx] = tag
                    else:
                        # --- 水平移動 (修正處) ---
                        # 原本漏了 [cz]，現在補上：在「當前樓層」打通中間牆壁
                        self.maze[cz][cy + dy][cx + dx] = 0
                        
                        # 設定目標點為路徑
                        self.maze[nz][ny][nx] = 0
                    
                    self._carve_passages_3d(nx, ny, nz)

    def draw_layers(self):
        print("正在繪製圖層...")
        cols = min(3, self.depth)
        rows = (self.depth + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
        # 處理只有一層或多層的情況，確保 axes 是列表
        if self.depth > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        cmap = mcolors.ListedColormap(['white', 'black', 'red', 'blue'])
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5] 
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        for z in range(self.depth):
            if z >= len(axes): break
            ax = axes[z]
            
            plot_data = [[0 for _ in range(self.width)] for _ in range(self.height)]
            tags_to_annotate = []

            for y in range(self.height):
                for x in range(self.width):
                    cell = self.maze[z][y][x]
                    if cell == 1:
                        plot_data[y][x] = 1 
                    elif cell == 0:
                        plot_data[y][x] = 0 
                    elif isinstance(cell, str):
                        if cell in ['IN', 'OUT']:
                             plot_data[y][x] = 3 
                             tags_to_annotate.append((x, y, cell))
                        else:
                            plot_data[y][x] = 2 
                            tags_to_annotate.append((x, y, cell))

            ax.imshow(plot_data, cmap=cmap, norm=norm)
            ax.set_title(f"Layer {z+1} (Depth index: {z})", fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            
            for tx, ty, tag_text in tags_to_annotate:
                color = 'white' if tag_text in ['IN', 'OUT'] else 'black'
                ax.text(tx, ty, tag_text, ha='center', va='center', 
                        color=color, fontsize=8, fontweight='bold')

        # 隱藏多餘子圖
        for i in range(self.depth, len(axes)):
            axes[i].axis('off')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    WIDTH = 21
    HEIGHT = 21
    DEPTH = 5 

    generator3d = Maze3DGenerator(WIDTH, HEIGHT, DEPTH)
    generator3d.generate(start_x=WIDTH//2, start_y=HEIGHT//2, start_z=0)
    generator3d.draw_layers()