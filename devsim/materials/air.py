from .base import Material


class _Air(Material):
    name = 'air'
    refractive_index = {}


Air = _Air()