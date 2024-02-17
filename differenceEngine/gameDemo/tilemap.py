import pygame as pg

NEIGHB_OFFSET = [
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (0, 0),
    (0, -1),
    (0, 1),
    (1, 0),
    (1, -1),
    (1, 1),
]
PHYSICTILE = {"grass", "stone"}


class tile_map:
    def __init__(self, game, tile_size=16) -> None:
        self.tile_size = tile_size
        self.tilemap = {}
        self.game = game
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[f"{3+i}_10"] = {
                "type": "grass",
                "variant": 0,
                "pos": (3 + i, 10),
            }
            self.tilemap[f"10_{i+5}"] = {
                "type": "grass",
                "variant": 1,
                "pos": (10, i + 5),
            }

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHB_OFFSET:
            check_loc = str(f"{tile_loc[0]+offset[0]}_{tile_loc[1]+offset[1]}")
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICTILE:
                rects.append(
                    pg.Rect(
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )
        return rects

    def render(self, surf):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size),
            )
