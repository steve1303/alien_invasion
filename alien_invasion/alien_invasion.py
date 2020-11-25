# coding=utf-8
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

        # 全屏 和下面那个框体内部的内容二选一
        """
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        """

        # 建立一个指定大小的显示窗口
        self.screen = pygame.display.set_mode(
                    (self.settings.screen_width, self.settings.screen_height))


        pygame.display.set_caption("Alien Invasion")  # 游戏框体左上角的游戏名

        # 创建一个用于存储游戏统计信息的实例
        # 创建记分牌
        self.stats = GameStats(self)  # self 必不可少
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # 子弹 继承精灵（sprite）类的实例
        self.aliens = pygame.sprite.Group()  # 外星人 继承精灵类的实例

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self, "Play")  # 创建play_button属性 指向实例化类Button 参数表示要显示的字样

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):  # 辅助方法 单下划线开头
        """响应键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # KEYDOWN事件 按下按键
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # KEYUP事件  松开按键
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()  # 重置速度
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

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
        if event.key == pygame.K_RIGHT:  # # K_RIGHT 左键
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # K_LEFT 左键
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # 按下Q键退出
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
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)   # 添加到编组

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并且计算一行可以容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
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
        self.aliens.add(alien)  # 添加到

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():  # 如果到达了边缘
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()   # 调用辅助函数

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)   # 一个字典

        if collisions:  # 子弹击落外星人，更新得分
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并且新建一群外星人
            self.bullets.empty()
            self._create_fleet()  # fleet 舰队
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 向飞船被撞倒一样处理
                self._ship_hit()
                break

    def _update_aliens(self):
        """检查是否有外星人位于屏幕的边缘，并更新外星人的位置。"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞。
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!")
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _update_screen(self):
        """每次循环时都重新绘制屏幕， 并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ship_left 减1 并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == "__main__":
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()  # 实例化类 建立对象ai 可以调用类中的属性和方法
    ai.run_game()         # 调用游戏主循环函数
