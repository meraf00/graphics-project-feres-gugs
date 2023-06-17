class World:
    def __init__(self):
        self.game_objects = {}
        self.last_id = 0

    def instantiate(self, game_object_class, *args, **kwargs):
        game_object = game_object_class(self.last_id, *args, **kwargs)

        self.game_objects[self.last_id] = game_object

        self.last_id += 1

    def dispose(self, game_object):
        if game_object.id in self.game_objects:
            del self.game_objects[game_object.id]


game_world: World = World()
