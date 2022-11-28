# Not a full class, but reusable function between any objects
def collide_objects(collider, item_collided):

    is_colliding = False
    if collider.colliderect(item_collided):
        # Basically just check if the moving object edge is within a set bounds of the other objects edge
        # Forces pacman (or a moving object) to edge of the item it collided with.
        if item_collided.left <= collider.right <= (item_collided.left + 5):  # Right Side
            collider.x = (collider.x - 4)
            is_colliding = True
        elif item_collided.right >= collider.left >= (item_collided.right - 5):  # Left
            collider.x = (collider.x + 4)
            is_colliding = True
        elif item_collided.bottom >= collider.top >= (item_collided.bottom - 5):  # Top
            collider.y = (collider.y + 4)
            is_colliding = True
        elif item_collided.top <= collider.bottom <= (item_collided.top + 5):  # Bottom
            collider.y = (collider.y - 4)
            is_colliding = True
        else:
            is_colliding = False

    return is_colliding
