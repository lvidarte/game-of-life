_glider = (
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 1) )

_lightweight_spaceship = (
        (1, 0, 0, 1, 0),
        (0, 0, 0, 0, 1),
        (1, 0, 0, 0, 1),
        (0, 1, 1, 1, 1) )

patterns = {
        'One cell': None,
        'Glider'  : _glider,
        'Lightweight spaceship': _lightweight_spaceship,
}
