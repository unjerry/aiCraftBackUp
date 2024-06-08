import numbers


class Block_type:
    def __init__(
        self, texture_magager, name="unknown", block_face_texture={"all": "cobblestone"}
    ) -> None:
        self.name = name
        self.vertex_positions = numbers.vertex_positions
        self.indices = numbers.indices
        for face in block_face_texture:
            texture = block_face_texture[face]
            texture_magager.add_texture(texture)
