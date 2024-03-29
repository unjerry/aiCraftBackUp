import pygame as pg


class orac:
    def __init__(self, layer, font, fontSize=20, string="None", pos=(0, 0)) -> None:
        self.fontSize = fontSize
        self.fontName = font
        self.layer = layer
        self.font = pg.font.Font(self.fontName, self.fontSize)
        self.content = string
        self.surf = self.font.render(self.content, True, "violet")
        self.pos = pos
        self.rect = self.surf.get_rect()
        self.rect.center = (0, 0)

    def render(self):
        self.layer.blit(self.surf, self.pos)

    def setContent(self, string):
        self.content = string
        self.surf = self.font.render(self.content, True, "violet")

    def setColor(self, color):
        self.surf = self.font.render(self.content, True, color)

    def setPos(self, pos):
        self.pos = pos
