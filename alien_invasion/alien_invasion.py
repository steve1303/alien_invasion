#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : fiuxiu
# @Time    : 2020年11月28日 22:51
# @Software: PyCharm

import sys
from time import sleep

import pygame

from setting import Setting
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:    # 外星人入侵
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 初始化背景设置
        self.settings = Setting()  # 设置setting属性指向一个实例化类Setting

        # 全屏
        """
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """
        # 调用pygame.display.set_mode建立一个指定大小（宽度，高度）的显示窗口  surface对象是Pygame中用于表示图像的对象
        # 在这个游戏中，每个元素如飞船或者外星人都是一个surface对象
        self.screen = pygame.display.set_mode(
                    (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")  # 游戏框体左上角的游戏名

        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)  # self  指的是当前AlienInvasion实例
        # 创建记分牌/计分板
        self.sb = Scoreboard(self)  # self  指的是当前AlienInvasion实例

        self.ship = Ship(self)  # 调用Ship()时 必须提供一个参数 这里是self  指的是当前AlienInvasion实例
        self.bullets = pygame.sprite.Group()  # 多个子弹 继承精灵（sprite）类的实例
        self.aliens = pygame.sprite.Group()  # 多个外星人 继承精灵（sprite）类的实例

        self._create_fleet()  # 调用 创建外星人群 的函数

        # 创建play按钮
        self.play_button = Button(self, "Play")  # 创建play_button属性 指向实例化类Button 参数表示要显示的字样

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:  # 游戏状态标志game_active为True时
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):  # 辅助方法 单下划线开头
        """响应键盘和鼠标事件"""
        for event in pygame.event.get():  # 利用for循环监听获取的每一个事件
            if event.type == pygame.QUIT:  # 调用
                self._save_high_socre()
                sys.exit()  # 调用系统退出接口
            elif event.type == pygame.KEYDOWN:  # KEYDOWN事件 按下按键
                self._check_keydown_events(event)  # 调用辅助函数
            elif event.type == pygame.KEYUP:  # KEYUP事件  松开按键
                self._check_keyup_events(event)  # 调用辅助函数
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 空格键
                mouse_pos = pygame.mouse.get_pos()  # pygame.mouse.get_pos() 获取鼠标光标的位置
                self._check_play_button(mouse_pos)  # 在玩家单击play按钮时开始新游戏

    def _check_play_button(self, mouse_pos):  # 实参为鼠标位置 开始新游戏的一系列准备
        """在玩家单击play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # 获取鼠标位置
        if button_clicked and not self.stats.game_active:  # 如果单击按钮并且游戏活动状态为False 未开始
            self._start_game()   # 调用下面的函数 开始新游戏

    def _start_game(self):
        """重置游戏的基本属性 开启一个新游戏"""
        # 重置速度
        self.settings.initialize_dynamic_settings()
        # 重置游戏统计信息
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()  # 调用ScoreBoard()类里面的函数 四个绘制操作
        # 清空余下的外星人和子弹
        self.aliens.empty()
        self.bullets.empty()
        # 创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()
        # 隐藏游戏光标
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按下按键。"""
        if event.key == pygame.K_RIGHT:  # K_RIGHT 左键
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # K_LEFT 左键
            self.ship.moving_left = True
        elif event.key == pygame.K_p:  # 按下P键 开始新游戏
            self._start_game()
        elif event.key == pygame.K_q:  # 按下Q键退出
            self._save_high_socre()
            sys.exit()
        elif event.key == pygame.K_SPACE:  # 按住空格键 开火
            self._fire_bullet()  # 调用开火函数

    def _check_keyup_events(self, event):
        """响应松开按键。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:  # 限制三颗子弹
            new_bullet = Bullet(self)  # 实例化子弹类
            self.bullets.add(new_bullet)   # 添加到子弹编组

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并且计算一行可以容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)  # 实例化外星人类 创建单个外星人
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)  # 屏幕宽度-外星人宽度的两倍
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)  # 添加行
        number_rows = available_space_y // (2 * alien_height)  # 计算行数

        # 创建外星人群(fleet舰队)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)  # 调用辅助函数_create_alien

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并且将其放到当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)  # 添加到外星人类

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():  # 如果到达了边缘
                self._change_fleet_direction()  # 调用下面的函数 改变方向和距离
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹（避免子弹堆积在顶部消耗内存）"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()   # 调用辅助函数 碰撞检测

    def _update_aliens(self):
        """检查是否有外星人位于屏幕的边缘，并更新外星人的位置。"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞。
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!")
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()  # 调用辅助函数检查

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)   # pygame.sprite.groupcollide() 一个字典
        # 子弹和外星人碰撞  哪个设置为Ture 哪个消失
        if collisions:  # 子弹击落外星人，更新得分
            for aliens in collisions.values():  # 遍历字典的值values
                self.stats.score += self.settings.alien_points * len(aliens)  # 每个外星人的得分*外星人数量
            self.sb.prep_score()  # 修改当前分数
            self.sb.check_high_score()  # 修改最高得分

        self.start_new_level()   # 调用下面的函数 开始一轮新的游戏 （代码的重构 结构更清晰）

    def start_new_level(self):
        if not self.aliens:  # 外星人杀光了一轮 开启一轮新游戏
            # 删除现有的子弹并且新建一群外星人
            self.bullets.empty()
            self._create_fleet()  # fleet 舰队
            self.settings.increase_speed()  # 调用提高速度的函数

            # 提高等级
            self.stats.level += 1  # 整群外星人被消灭 计分板等级显示提高1
            self.sb.prep_level()  # 调用函数 渲染图形

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()  # 获取屏幕矩形的属性
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:  # 检测只要有一个到达了底端
                # 向飞船被撞倒一样处理
                self._ship_hit()   # 调用辅助函数 飞船被摧毁了
                break

    def _update_screen(self):
        """每次循环时都重新绘制屏幕， 并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)  # 重新绘制屏幕 参数为背景颜色
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # 绘制子弹

        # 显示得分
        self.sb.show_score()  # 调用scoreboard类中的函数show_score

        # 如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # 调用函数让最近绘制的屏幕可见

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:  # 游戏状态 剩余飞船数>0
            # 将ship_left 减1 并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()  # 调用函数

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部的中央
            self._create_fleet()  # 调用辅助方法 创建新的一群外星人
            self.ship.center_ship()  # 调用辅助方法 飞船居中

            # 暂停0.5s
            sleep(0.5)
        else:
            self.stats.game_active = False  # 游戏活动状态为False
            pygame.mouse.set_visible(True)  # 参数为True，显示鼠标光标

    def _save_high_socre(self):  # 单下划线开头 半私有的辅助方法
        """写入游戏最高分"""
        file_name = r"high_score.txt"
        with open(file_name, "w") as f:
            f.write(f"{self.stats.high_score}\n")


if __name__ == "__main__":
    ai = AlienInvasion()  # 创建游戏实例
    ai.run_game()         # 运行游戏 主循环
