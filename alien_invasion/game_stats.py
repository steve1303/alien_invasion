# coding=utf-8


class GameStats:
    """"跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        # 在任何情况不应该重置最高得分 在init中设置而不是reset_stats()中
        self.high_score = 0
        self.settings = ai_game.settings  # 为了调用settings.py文件里面类的方法
        self.reset_stats()  # 调用函数

        # 游戏刚启动时处于活动状态
        self.game_active = False  # 标志

    def reset_stats(self):
        """在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
