import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import pygame.locals
from PIL import Image, ImageTk
import random

class PygameApp:
    def __init__(self, master):
        self.master = master
        master.title("Square Shooter in Pygame-Tkinter")

        # Create a Tkinter canvas
        self.canvas = tk.Canvas(master, width=400, height=300)
        self.canvas.pack(side=tk.TOP)

        # Initialize Pygame
        pygame.init()

        # Create a Pygame surface
        self.screen = pygame.Surface((400, 300))

        # Initialize player square
        self.player_pos = [175, 250]
        self.player_size = 30
        self.move_distance = 5

        # Initialize enemy square
        self.enemy_pos = [random.randint(0, 370), 50]
        self.enemy_size = 30

        # Initialize bullets
        self.bullets = []
        self.bullet_size = 5
        self.bullet_speed = 7

        # Create directional and shoot buttons
        button_frame = ttk.Frame(master)
        button_frame.pack(side=tk.BOTTOM)

        self.up_button = ttk.Button(button_frame, text="Up", command=self.move_up)
        self.up_button.grid(row=0, column=1)

        self.left_button = ttk.Button(button_frame, text="Left", command=self.move_left)
        self.left_button.grid(row=1, column=0)

        self.right_button = ttk.Button(button_frame, text="Right", command=self.move_right)
        self.right_button.grid(row=1, column=2)

        self.down_button = ttk.Button(button_frame, text="Down", command=self.move_down)
        self.down_button.grid(row=2, column=1)

        self.shoot_button = ttk.Button(button_frame, text="Shoot", command=self.shoot)
        self.shoot_button.grid(row=1, column=1)

        # Start the Pygame loop
        self.update()

    def move_up(self):
        self.player_pos[1] = max(0, self.player_pos[1] - self.move_distance)

    def move_down(self):
        self.player_pos[1] = min(300 - self.player_size, self.player_pos[1] + self.move_distance)

    def move_left(self):
        self.player_pos[0] = max(0, self.player_pos[0] - self.move_distance)

    def move_right(self):
        self.player_pos[0] = min(400 - self.player_size, self.player_pos[0] + self.move_distance)

    def shoot(self):
        bullet_x = self.player_pos[0] + self.player_size // 2 - self.bullet_size // 2
        bullet_y = self.player_pos[1] - self.bullet_size
        self.bullets.append([bullet_x, bullet_y])

    def update(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))  # White background

        # Draw the player square
        pygame.draw.rect(self.screen, (0, 0, 255), (self.player_pos[0], self.player_pos[1], self.player_size, self.player_size))

        # Draw the enemy square
        pygame.draw.rect(self.screen, (255, 0, 0), (self.enemy_pos[0], self.enemy_pos[1], self.enemy_size, self.enemy_size))

        # Update and draw bullets
        for bullet in self.bullets[:]:
            bullet[1] -= self.bullet_speed
            pygame.draw.rect(self.screen, (0, 255, 0), (bullet[0], bullet[1], self.bullet_size, self.bullet_size))
            
            # Remove bullets that are off-screen
            if bullet[1] < 0:
                self.bullets.remove(bullet)
            
            # Check for collision with enemy
            if (self.enemy_pos[0] < bullet[0] < self.enemy_pos[0] + self.enemy_size and
                self.enemy_pos[1] < bullet[1] < self.enemy_pos[1] + self.enemy_size):
                self.bullets.remove(bullet)
                self.enemy_pos = [random.randint(0, 370), 50]  # Respawn enemy

        # Check for collision between player and enemy
        if (self.player_pos[0] < self.enemy_pos[0] + self.enemy_size and
            self.player_pos[0] + self.player_size > self.enemy_pos[0] and
            self.player_pos[1] < self.enemy_pos[1] + self.enemy_size and
            self.player_pos[1] + self.player_size > self.enemy_pos[1]):
            messagebox.showinfo("Game Over", "You've been hit!")
            self.master.quit()
            return

        # Convert Pygame surface to PIL Image
        pygame_surface_3d = pygame.image.tostring(self.screen, 'RGB')
        pil_image = Image.frombytes('RGB', (400, 300), pygame_surface_3d)

        # Convert PIL Image to Tkinter-compatible PhotoImage
        self.photo = ImageTk.PhotoImage(pil_image)

        # Update the Tkinter canvas with the new image
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the next update
        self.master.after(16, self.update)  # ~60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    app = PygameApp(root)
    root.mainloop()