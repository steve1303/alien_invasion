# coding=utf-8
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):  # 继承自精灵类
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings  # 便于在update（）访问外星人的速度

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('./images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕的边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """向左或者向右移动外星人"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)  # 移动量
        self.rect.x = self.x
