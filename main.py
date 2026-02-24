import pygame
import random


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber-Aegis: Arcade Edition")


ORANGE_POP = (255, 165, 0)  
BLEU_ROYAL = (0, 102, 204)   
ROUGE_DANGER = (220, 20, 60) 
VERT_FLASH = (50, 255, 50)   
NOIR_TEXTE = (20, 20, 20)    
BLANC = (255, 255, 255)     


font = pygame.font.SysFont("Arial", 26, bold=True)
font_big = pygame.font.SysFont("Arial", 60, bold=True)



class Player:
    def __init__(self):
        self.width = 50
        self.height = 45
        self.x = WIDTH // 2
        self.y = HEIGHT - 70
        self.speed = 9

    def draw(self):
        
        pygame.draw.polygon(screen, BLEU_ROYAL, [
            (self.x, self.y + self.height), 
            (self.x + self.width // 2, self.y), 
            (self.x + self.width, self.y + self.height)
        ])

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0: self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width: self.x += self.speed

class Enemy:
    def __init__(self):
        self.size = 40
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(-500, -50)
        self.speed = random.randint(4, 7)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT: self.reset()

    def draw(self):
        
        pygame.draw.rect(screen, ROUGE_DANGER, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, NOIR_TEXTE, (self.x, self.y, self.size, self.size), 2)

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -12

    def update(self):
        self.y += self.speed

    def draw(self):
       
        pygame.draw.rect(screen, VERT_FLASH, (self.x, self.y, 5, 18))



def reset_game():
    
    return Player(), [Enemy() for _ in range(8)], [], 0, False

player, enemies, lasers, score, game_over = reset_game()
clock = pygame.time.Clock()
running = True



while running:
    
    screen.fill(ORANGE_POP)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Tirer (Espace)
            if event.key == pygame.K_SPACE and not game_over:
                lasers.append(Laser(player.x + 22, player.y))
            # Recommencer (R)
            if event.key == pygame.K_r and game_over:
                player, enemies, lasers, score, game_over = reset_game()

    if not game_over:
        
        player.move()

       
        for l in lasers[:]:
            l.update()
            if l.y < 0: lasers.remove(l)

        
        for e in enemies:
            e.update()
            
            
            for l in lasers[:]:
                if e.x < l.x < e.x + e.size and e.y < l.y < e.y + e.size:
                    score += 10
                    e.reset()
                    if l in lasers: lasers.remove(l)

            
            if (e.y + e.size > player.y and e.x < player.x + 50 and e.x + e.size > player.x):
                game_over = True

        
        player.draw()
        for e in enemies: e.draw()
        for l in lasers: l.draw()
        
    else:
       
        msg = font_big.render("TU ES NUL, RECOMMENCE", True, NOIR_TEXTE)
        retry_msg = font.render("Appuie sur 'R' pour retenter ta chance !", True, BLANC)
        
        
        screen.blit(msg, (WIDTH//2 - 320, HEIGHT//2 - 50))
        screen.blit(retry_msg, (WIDTH//2 - 200, HEIGHT//2 + 40))

    
    score_txt = font.render(f"SCORE: {score}", True, NOIR_TEXTE)
    screen.blit(score_txt, (15, 15))

    pygame.display.flip()
    clock.tick(60) 

pygame.quit()