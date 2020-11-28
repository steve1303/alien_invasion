# -*- coding: utf-8 -*-
import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分相关信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)  # 从系统字体库创建一个 Font 对象

        self.prep_images()  # 调用下面的函数 (代码的重构)

    def prep_images(self):
        """绘制最高得分，当前得分,飞船数量，当前等级这四个图像"""
        self.prep_ships()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()  # 创建一个空编组
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10  # 距离顶部10px
            self.ships.add(ship)  # 添加到编组ships

    # Pygame通过将你要显示的字符串渲染为图像来处理文本。
    def prep_score(self):
        """将当前得分转化为渲染的图像"""
        rounded_score = round(self.stats.score, -1)  # round() 方法返回浮点数x的四舍五入值
        score_str = "{:,}".format(rounded_score)  # 字符类型的文字
        # score_str = str(self.stats.score)

        # 方法font.render() 还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能(反锯齿让文本的边缘更平滑)。
        # 余下的两个实参分别是文本颜色和背景色。
        # 我们启用了反锯齿功能，并将文本的背景色设置为按钮的颜色(如果没有指定背景色，Pygame将以透明背景的方式渲染文本
        self.score_image = self.font.render(f"Score: {score_str}", True,
                    self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()  # 获取分数对象的矩形
        self.score_rect.right = self.screen_rect.right - 20  # 离右边的距离为20px
        self.score_rect.top = 20  # 离顶部的距离为20px

    def prep_high_score(self):
        """将最高得分转化为渲染的图像"""
        high_score = round(self.stats.high_score, -1)  # 让小数精确到小数点后的某一位  实参指定为-1 10的整数倍
        high_score_str = "{:,}".format(high_score)
        # score_str = str(self.stats.score)
        self.high_score_image = self.font.render(f"High Score: {high_score_str}", True,
                        self.text_color, self.settings.bg_color)

        # 在屏幕顶部中央显示得分
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转化为渲染的图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Level: {level_str}", True,
                    self.text_color, self.settings.bg_color)

        # 将等级放在得分的下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  # 等级在当前得分底端位置 + 10

    def show_score(self):
        """在屏幕上显示得分，等级和余下的飞船数"""
        # surface.blit(image,(x,y),rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """检查是否有了最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
