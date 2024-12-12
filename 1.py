import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 游戏设置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# 定义方块颜色
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetromino:
    def __init__(self):
        self.reset()

    def reset(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.shape_idx]]
        self.color = SHAPE_COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self, grid):
        old_shape = [row[:] for row in self.shape]
        self.shape = [[self.shape[y][x] for y in range(len(self.shape)-1, -1, -1)]
                     for x in range(len(self.shape[0]))]
        if not self.valid_move(self.x, self.y, grid):
            self.shape = old_shape

    def draw(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, self.color,
                                   (BLOCK_SIZE * (self.x + j),
                                    BLOCK_SIZE * (self.y + i),
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def move(self, dx, dy, grid):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.valid_move(new_x, new_y, grid):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def valid_move(self, new_x, new_y, grid):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if (new_x + j < 0 or new_x + j >= GRID_WIDTH or
                        new_y + i >= GRID_HEIGHT or
                        grid[new_y + i][new_x + j] != BLACK):
                        return False
        return True

def check_lines(grid, score):
    lines_cleared = 0
    y = GRID_HEIGHT - 1
    while y >= 0:
        if all(cell != BLACK for cell in grid[y]):
            del grid[y]
            grid.insert(0, [BLACK] * GRID_WIDTH)
            lines_cleared += 1
        else:
            y -= 1
    
    if lines_cleared == 1:
        score += 100
    elif lines_cleared == 2:
        score += 300
    elif lines_cleared == 3:
        score += 500
    elif lines_cleared == 4:
        score += 800
    
    return score

def draw_next_piece(screen, next_piece):
    next_x = BLOCK_SIZE * (GRID_WIDTH + 1)
    next_y = BLOCK_SIZE * 2
    
    font = pygame.font.Font(None, 36)
    text = font.render("下一个:", True, WHITE)
    screen.blit(text, (next_x, BLOCK_SIZE))
    
    for i in range(len(next_piece.shape)):
        for j in range(len(next_piece.shape[0])):
            if next_piece.shape[i][j]:
                pygame.draw.rect(screen, next_piece.color,
                               (next_x + j * BLOCK_SIZE,
                                next_y + i * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))

def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(text, (BLOCK_SIZE * (GRID_WIDTH + 1), BLOCK_SIZE * 6))

try:
    # 创建游戏窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('俄罗斯方块')

    # 初始化游戏
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_piece = Tetromino()
    next_piece = Tetromino()
    score = 0

    # 游戏主循环
    running = True
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 500

    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time >= fall_speed:
            if not current_piece.move(0, 1, grid):
                for i in range(len(current_piece.shape)):
                    for j in range(len(current_piece.shape[0])):
                        if current_piece.shape[i][j]:
                            grid[current_piece.y + i][current_piece.x + j] = current_piece.color
                
                score = check_lines(grid, score)
                current_piece = next_piece
                next_piece = Tetromino()
                
                if not current_piece.valid_move(current_piece.x, current_piece.y, grid):
                    running = False
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0, grid)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0, grid)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1, grid)
                elif event.key == pygame.K_UP:
                    current_piece.rotate(grid)
                elif event.key == pygame.K_SPACE:
                    while current_piece.move(0, 1, grid):
                        pass

        screen.fill(BLACK)
        
        # 绘制已固定的方块
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if grid[i][j] != BLACK:
                    pygame.draw.rect(screen, grid[i][j],
                                   (j * BLOCK_SIZE, i * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # 绘制当前方块
        current_piece.draw(screen)
        
        # 绘制游戏区域边框
        pygame.draw.rect(screen, WHITE, (0, 0, BLOCK_SIZE * GRID_WIDTH, SCREEN_HEIGHT), 1)
        
        # 绘制下一个方块预览和分数
        draw_next_piece(screen, next_piece)
        draw_score(screen, score)
        
        pygame.display.flip()

except Exception as e:
    print(f"发生错误: {e}")

finally:
    pygame.quit()