import pygame
import pyrebase
from pygame.locals import *
from tkinter import *
import sys
import time
import random

firebaseConfig = {
    "apiKey": "AIzaSyCnzRFUr6lqt0rbfOM3MFrLRDejPK9oId0",
    "authDomain": "python-project-d0a65.firebaseapp.com",
    "databaseURL": "https://python-project-d0a65-default-rtdb.firebaseio.com/",
    "projectId": "python-project-d0a65",
    "storageBucket": "python-project-d0a65.appspot.com",
    "messagingSenderId": "871454565653",
    "appId": "1:871454565653:web:05e402953aae3b6b99b51c",
    "measurementId": "G-SFK6M5K9SG"
}
firebase = pyrebase.initialize_app(firebaseConfig)


class Game:

    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.end = False
        self.email = ''
        self.pwd = ''
        self.C_pwd = ''
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.HEAD_C = (255, 0, 0)
        self.RECT_C = (0, 0, 255)
        self.TEXT_C = (0, 50, 200)
        self.RESULT_C = (255, 70, 70)
        self.clock = pygame.time.Clock()
        self.user = firebase.auth()

        pygame.init()
        self.open_img = pygame.image.load('unnamed.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('shutterstock_262946390.jpg')
        self.bg = pygame.transform.scale(self.bg, (750, 500))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Type Speed test')

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def login(self):

        self.E_active = False
        self.P_active = False

        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)

        self.screen.blit(self.bg, (0, 0))
        self.draw_text(self.screen, "LOGIN", 80, 80, self.HEAD_C)
        self.screen.fill((0, 50, 250), (300, 330, 150, 40))
        pygame.draw.rect(self.screen, (0,0,0), (300, 330, 150, 40),2 )
        self.draw_text(self.screen, "Login",350, 26, (255, 255, 255))

        self.draw_text(self.screen, 'Email Address', 135, 25, (0, 0, 0))
        self.draw_text(self.screen, 'Password', 228, 25, (0, 0, 0))
        self.draw_text(self.screen, "--------------------", 380, 35, (0, 0, 0))
        self.draw_text(self.screen, " Don\'t have a account yet?", 400, 20, (0, 0, 0))

        self.screen.fill((0, 0, 0), (300, 415, 150, 40))
        pygame.draw.rect(self.screen, self.RECT_C, (300, 415, 150, 40),2 )
        self.draw_text(self.screen, "SignUp",435, 26, (255, 255, 255))

        self.running = True
        while (self.running):

            self.screen.fill((0, 0, 0), (140, 150, 470, 50))
            pygame.draw.rect(self.screen, self.RECT_C, (140, 150, 470, 50), 2)
            self.draw_text(self.screen, self.email, 175, 26, (250, 250, 250))

            self.screen.fill((0, 0, 0), (140, 240, 470, 50))
            pygame.draw.rect(self.screen, self.RECT_C, (140, 240, 470, 50), 2)
            self.draw_text(self.screen, self.pwd, 265, 26, (250, 250, 250))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if (x >= 140 and x <= 470 and y >= 150 and y <= 190):
                        self.E_active = True
                        self.P_active = False
                        self.email = ''
                    if (x >= 140 and x <= 470 and y >= 240 and y <= 280):
                        self.P_active = True
                        self.E_active = False
                        self.pwd = ''
                    if (x >= 300 and x <= 450 and y >= 330 and y<=370):
                        try:
                            login = self.user.sign_in_with_email_and_password(self.email, self.pwd)
                            self.run()
                        except:
                            self.draw_text(self.screen, 'Invalid Email or Password',20,26,self.TEXT_C)
                            pygame.display.update()
                        x, y = pygame.mouse.get_pos()
                    if (x >= 300 and x <= 450 and y >= 415 and y <= 455):
                        self.Signup()
                        x, y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:

                    if self.E_active and not self.P_active:
                        if event.key == pygame.K_RETURN:
                            print(self.email)
                            self.E_active = False

                        elif event.key == pygame.K_BACKSPACE:
                            self.email = self.email[:-1]
                        else:
                            try:
                                self.email += event.unicode
                            except:
                                pass
                    elif self.P_active and not self.E_active:
                        if event.key == pygame.K_RETURN:
                            print(self.pwd)
                            self.P_active = False

                        elif event.key == pygame.K_BACKSPACE:
                            self.pwd = self.pwd[:-1]
                        else:
                            try:
                                self.pwd += event.unicode
                            except:
                                pass

        pygame.display.update()

    def Signup(self):

        self.E_active = False
        self.P_active = False
        self.CP_active = False

        self.screen.blit(self.bg, (0, 0))
        self.draw_text(self.screen, "Create Account", 60, 80, self.HEAD_C)
        self.screen.fill((0, 50, 250), (300, 365, 150, 40))
        pygame.draw.rect(self.screen, (0, 0, 0), (300, 365, 150, 40), 2)
        self.draw_text(self.screen, "SignUp", 385, 26, (255, 255, 255))

        self.draw_text(self.screen, 'Email Address', 125, 25, (0, 0, 0))
        self.draw_text(self.screen, 'Password', 205, 25, (0, 0, 0))
        self.draw_text(self.screen, 'Confirm Password', 285, 25, (0, 0, 0))
        self.draw_text(self.screen, "--------------------", 415, 35, (0, 0, 0))
        self.draw_text(self.screen, " Already have an account?", 430, 18, (0, 0, 0))

        self.screen.fill((0, 0, 0), (300, 445, 150, 40))
        pygame.draw.rect(self.screen, self.RECT_C, (300, 445, 150, 40), 2)
        self.draw_text(self.screen, "Login", 465, 26, (255, 255, 255))

        self.running = True
        while (self.running):

            self.screen.fill((0, 0, 0), (140, 135, 470, 50))
            pygame.draw.rect(self.screen, self.RECT_C, (140, 135, 470, 50), 2)
            self.draw_text(self.screen, self.email, 160, 26, (250, 250, 250))

            self.screen.fill((0, 0, 0), (140, 215, 470, 50))
            pygame.draw.rect(self.screen, self.RECT_C, (140, 215, 470, 50), 2)
            self.draw_text(self.screen, self.pwd, 240, 26, (250, 250, 250))

            self.screen.fill((0, 0, 0), (140, 295, 470, 50))
            pygame.draw.rect(self.screen, self.RECT_C, (140, 295, 470, 50), 2)
            self.draw_text(self.screen, self.C_pwd, 320, 26, (250, 250, 250))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if (x >= 140 and x <= 470 and y >= 135 and y <= 185):
                        self.E_active = True
                        self.P_active = False
                        self.CP_active = False
                        self.email = ''
                    if (x >= 140 and x <= 470 and y >= 215 and y <= 265):
                        self.P_active = True
                        self.E_active = False
                        self.CP_active = False
                        self.pwd = ''
                    if (x >= 140 and x <= 470 and y >= 295 and y <= 345):
                        self.P_active = False
                        self.E_active = False
                        self.CP_active = True
                        self.C_pwd = ''
                    if (x >= 300 and x <= 450 and y >= 365 and y <= 405):
                        try:
                            if(self.pwd == self.C_pwd):
                                create = self.user.create_user_with_email_and_password(self.email, self.pwd)
                                self.run()
                        except:
                            if(self.pwd == self.C_pwd):
                                self.draw_text(self.screen, 'Account already exits', 20, 26, self.TEXT_C)
                            else:
                                self.draw_text(self.screen, 'password and confirm password don\'t match', 20, 26, self.TEXT_C)
                        x, y = pygame.mouse.get_pos()
                    if (x >= 300 and x <= 450 and y >= 445 and y <= 485):
                        self.login()
                        x, y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:

                    if self.E_active and not self.P_active and not self.CP_active:
                        if event.key == pygame.K_RETURN:
                            print(self.email)
                            self.E_active = False

                        elif event.key == pygame.K_BACKSPACE:
                            self.email = self.email[:-1]
                        else:
                            try:
                                self.email += event.unicode
                            except:
                                pass
                    elif self.P_active and not self.E_active and not self.CP_active:
                        if event.key == pygame.K_RETURN:
                            print(self.pwd)
                            self.P_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.pwd = self.pwd[:-1]
                        else:
                            try:
                                self.pwd += event.unicode
                            except:
                                pass
                    elif self.CP_active and not self.E_active and not self.P_active:
                        if event.key == pygame.K_RETURN:
                            print(self.C_pwd)
                            self.P_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.C_pwd = self.C_pwd[:-1]
                        else:
                            try:
                                self.C_pwd += event.unicode
                            except:
                                pass
        pygame.display.update()

    def show_results(self, screen):
        if (not self.end):
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(
                round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            # screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))

            print(self.results)
            pygame.display.update()

    def run(self):
        #self.login()
        self.reset_game()
        self.end = False
        self.running = True

        while (self.running):

            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.RECT_C, (50, 250, 650, 50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if (x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                        # position of reset box
                    if (x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()


                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        self.clock.tick(60)

    def reset_game(self):


        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # drawing heading
        self.screen.fill((0, 255, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C) # TEXT COLOUR
        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)

        # draw the sentence string
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()




Game().login()



