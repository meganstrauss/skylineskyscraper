from enemy import Enemy
class Snail(Enemy):
    url = 'blooper.png'
    #taken from https://www.mariowiki.com/images/a/af/PMCS_Blooper.png
    def getSprites(width, height):
        Snail.width = width
        Snail.height = height
        sprites = [(0, 0, width, height)]
        return sprites