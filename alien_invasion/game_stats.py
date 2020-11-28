# coding=utf-8


class GameStats:
    """"跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        # 在任何情况不应该重置最高得分 在init中设置而不是reset_stats()中
        self.high_score = self._read_high_score()  # 调初始化最高分时 用函数读取文件中的值
        self.settings = ai_game.settings  # 为了调用settings.py文件里面类的方法
        self.reset_stats()  # 调用函数

        # 游戏刚启动时处于活动状态
        self.game_active = False  # 标志

    def reset_stats(self):
        """在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _read_high_score(self):  # 单下划线开头 半私有方法 外部import不会导入 基本只在类内部访问
        """定义函数读取文件中的最高分数值"""
        file_name = r"high_score.txt"
        with open(file_name, "r") as f:
            high_score = f.read()
        return int(high_score)  # 函数返回值为字符串类型 转换为int

