import pygame
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
BLOCK_SIZE = 30  # 每个方块的大小
GRID_WIDTH = 10  # 游戏区域宽度（以方块数计）
GRID_HEIGHT = 20  # 游戏区域高度（以方块数计）
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)  # 屏幕宽度
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT  # 屏幕高度

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 游戏主循环
running = True
clock = pygame.time.Clock()

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 清空屏幕
    screen.fill(BLACK)
    
    # 绘制游戏区域边框
    pygame.draw.rect(screen, WHITE, (0, 0, BLOCK_SIZE * GRID_WIDTH, SCREEN_HEIGHT), 1)
    
    # 更新显示
    pygame.display.flip()
    
    # 控制游戏速度
    clock.tick(60)

# 退出游戏
pygame.quit()