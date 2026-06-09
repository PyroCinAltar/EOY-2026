import pygame
import pytmx


class TileMap:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename)

        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

        self.walls = []
        self.enemy_spawns = []
        self.player_spawn = (100, 100)
        self.exit_rect = None

        self.load_collision_tiles()
        self.load_objects()

    # ---------------- TILE COLLISION ----------------
    def load_collision_tiles(self):
        layer = self.tmx.get_layer_by_name("WallMap")

        for y in range(layer.height):
            for x in range(layer.width):

                gid = layer.data[y][x]

                if gid != 0:  # 0 = empty tile
                    self.walls.append(
                        pygame.Rect(
                            x * self.tmx.tilewidth,
                            y * self.tmx.tileheight,
                            self.tmx.tilewidth,
                            self.tmx.tileheight
                        )
                    )
        

    # ---------------- OBJECTS ----------------
    def load_objects(self):

        if self.tmx.get_layer_by_name("Spawns"):
            for obj in self.tmx.get_layer_by_name("Spawns"):

                if obj.name == "PlayerSpawn":
                    self.player_spawn = (obj.x, obj.y)

                elif obj.type == "EnemySpawn":
                    self.enemy_spawns.append((obj.x, obj.y))

        if self.tmx.get_layer_by_name("ExitDoors"):
            for obj in self.tmx.get_layer_by_name("ExitDoors"):
                self.exit_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    # ---------------- DRAW MAP ----------------
    def draw(self, screen, camera):
        for layer in self.tmx.visible_layers:

        # Only tile layers
            if layer.__class__.__name__ == "TiledTileLayer":

                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)

                    if tile:
                        screen.blit(
                            tile,
                            (
                                x * self.tmx.tilewidth - camera.offset.x,
                                    y * self.tmx.tileheight - camera.offset.y
                            )
                        )
            # exit 
        #     if self.tmx.get_layer_by_name("ExitDoors"):
        #         for obj in self.tmx.get_layer_by_name("ExitDoors"):
        #             self.exit_rect = pygame.Rect(
        #                 obj.x,
        #                 obj.y,
        #                 obj.width,
        #                 obj.height
        # )
             
                
        #    Wall debug
    # def draw_walls(self, screen, camera):
    #     for w in self.walls:
    #         pygame.draw.rect(
    #             screen,
    #                 (255, 0, 0),
    #             w.move(-camera.offset.x, -camera.offset.y),
    #             1
    #         )
    
    