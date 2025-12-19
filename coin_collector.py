import arcade
import random

SCREEN_WIDTH = 725
SCREEN_HEIGHT = 607

class MyGame(arcade.Window):
    

    def __init__(self):
        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Խաղ")
        

        self.set_mouse_visible(False)
        

        self.background = arcade.load_texture("./water.jpg")
        

        self.coin_sound = arcade.load_sound(":resources:sounds/coin3.wav")
        self.enemy_sound = arcade.load_sound(":resources:sounds/hurt4.wav")
        self.bullet_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/error4.wav")
         
   
            
    def setup(self):

        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.counter = 0
        self.enemies = 10

        self.paused = False        
        self.quit = False        
        self.restart = False
        self.won = False
        
        self.player_sprite = arcade.Sprite(":resources:images/enemies/fishGreen.png", 0.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)
        
        for i in range(40):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.3)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.velocity = (0, random.randint(-5,-1))
            self.coin_list.append(coin)

        for i in range(10):
            enemy = arcade.Sprite(":resources:images/enemies/slimeBlue.png", 0.4)
            enemy.center_x = random.randint(0,725)
            enemy.center_y = random.randint(0,607)
            enemy.velocity = (0, random.randint(1,3))
            self.enemies_list.append(enemy)


        
    def on_draw(self):
        
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)
        
        
        
        self.player_list.draw()
        self.coin_list.draw()
        self.enemies_list.draw()
        self.bullet_list.draw()
        
        
        output = f"Միավորներ: {self.counter}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        output2 = f"Հակառակորդներ: {self.enemies}"
        arcade.draw_text(output2, 150, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Left click: shoot    P: Pause    Q: Quit    R: Restart", 10, 580, arcade.color.WHITE, 14)

        if self.paused:
            arcade.draw_text("Դադար", 130, 330, arcade.color.WHITE, 100)
            arcade.draw_text("Սեղմե՛ք P խաղին վերադառնալու համար:", 50, 220, arcade.color.WHITE, 25)
        
        if self.quit:            
            arcade.draw_text("Եթե իրոք ցանկանում եք դուրս գալ խաղից,", 50, 180, arcade.color.RED, 23)
            arcade.draw_text("ապա սեղմե՛ք ENTER:", 230, 140, arcade.color.RED, 23)

        if self.restart:            
            arcade.draw_text("Եթե իրոք ցանկանում եք վերագործարկել", 50, 180, arcade.color.YELLOW, 23)
            arcade.draw_text("խաղը, ապա սեղմե՛ք ENTER:", 180, 140, arcade.color.YELLOW, 23)

        if self.won:
            arcade.draw_text("Դու հավաքեցի՛ր բոլոր մետաղադրամները", 30, 400, arcade.color.YELLOW, 25)
            arcade.draw_text("Խաղն ավարտված է", 190, 350, arcade.color.YELLOW, 27)
        
    def update(self, delta_time):

        if self.paused:
            self.won = False
            return

        if len(self.coin_list) == 0:
            self.won = True
       
        self.coin_list.update()
        self.enemies_list.update()
        self.bullet_list.update()
        
        for i in self.coin_list:
            if i.center_y<0:
                i.center_y=SCREEN_HEIGHT
                
        for i in self.enemies_list:
            if i.center_y>SCREEN_HEIGHT:
                i.center_y=0
        
        coins_hit_list = self.player_sprite.collides_with_list(self.coin_list)

        for i in coins_hit_list:
            i.remove_from_sprite_lists() 
            self.counter += 1
            arcade.play_sound(self.coin_sound)
            
        enemies_hit_list = self.player_sprite.collides_with_list(self.enemies_list)

        if len(enemies_hit_list)>0:
            self.counter = 0
            arcade.play_sound(self.enemy_sound)
            
        if len(self.coin_list)==0:
            for i in self.enemies_list:
                i.remove_from_sprite_lists()

        for i in self.bullet_list:
            enemies_hit_by_bullet = i.collides_with_list(self.enemies_list)
            for j in enemies_hit_by_bullet:
                j.remove_from_sprite_lists()
                self.enemies -= 1
                arcade.play_sound(self.hit_sound)
            if len(enemies_hit_by_bullet)>0:
                i.remove_from_sprite_lists()
    
            
    def on_mouse_motion(self, x, y, dx, dy):

        if self.paused:
            return
       
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


    def on_mouse_press(self, x, y, button, modifiers):
        if self.paused:
            return
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = arcade.Sprite(":resources:images/space_shooter/meteorGrey_tiny1.png", 0.5)
            bullet.center_x = x
            bullet.center_y = y
            bullet.velocity = (0, 10)
            self.bullet_list.append(bullet)
            arcade.play_sound(self.bullet_sound)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.paused = not self.paused
            self.quit = False
            self.restart = False
            
        if key == arcade.key.Q:
            self.paused = True
            self.quit = True
            self.restart = False
        if key == arcade.key.ENTER and self.quit == True:
            arcade.close_window()
        if key == arcade.key.R:
            self.paused = True
            self.restart = True
            self.quit=False

        if key == arcade.key.ENTER and self.restart == True:

            self.setup()

def main():
    
    window = MyGame()
    window.setup()
    arcade.run()

main()
