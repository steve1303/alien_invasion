# coding=utf-8


class Setting:
    """存储游戏《外星人入侵》中的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船设置（有几条命）
        self.ship_limit = 3
        # 子弹设置 宽3px，高15px 深灰色的子弹，速度比飞船速度稍慢
        self.bullet_width = 5    # 子弹宽度 500
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5  # 限制子弹数量

        # 外星人下落速度设置
        self.fleet_drop_speed = 10

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1  # 速度增加的倍率
        self.score_sacle = 1.5

        self.initialize_dynamic_settings()  # 调用函数

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5   # 初始速度
        self.bullet_speed = 3.0
        self.alien_speed = 1.5

        # fleet_direction 为1 表示向右移动， -1 表示向左移动
        self.fleet_direction = 1

        # 一个外星人的分值 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度和外星人分数设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_sacle)
        # print(self.alien_points)