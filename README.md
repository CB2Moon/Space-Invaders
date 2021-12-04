# Space-Invaders

## Interface

### Version 1 (TASK=1)

![](https://user-images.githubusercontent.com/95510991/144702593-9b9fe920-4e36-4d89-a870-9d9901c3a5ff.png)

### Version 2 (TASK=2)

Make it prettier.

![](https://user-images.githubusercontent.com/95510991/144702573-e4bc75d6-31c8-480d-aa91-7869a4fa1244.png)

### Version 3 (TASK=3)

Add lives.

![](https://user-images.githubusercontent.com/95510991/144702614-f12c0914-14dc-4286-a669-eda22b48b2a8.png)

## Introduction

The goal of the game is to collect a specified amount of collectable entities without having a destroyable entity reach the player’s row. If a red destroyable entity reaches the player’s row then the game is over. If any other entity reaches the top row then the game continues as normal. 

Players mainly interact with the game by moving _non-player entities_ on the grid. It is important to note that the player never moves and remains centered on the grid in the top row. Entities are rotated left and right and _wrap_ around to the other side of the grid if they are moved off an edge.

### Piece Types (non-player entities)

*   **Destroyable (D):** Red entity that players must destroy before it reaches the top row where the player is located.
*   **Collectable (C):** Blue entity that players must collect. By default, collecting 7 Collectables will cause the Player to win the game.
*   **Blocker (B):** Grey entity that players cannot shoot through.

### **Shot type**

*   **Destroy:** used to destroys everything except Blocker type entities.
*   **Collect:** used to collect collectable type entities.

### Key Press

*   **"A"**: All non-player entities rotate **left** one square.
*   **"D"**: All non-player entities rotate **right** one square.
*   **"SPACE"**: Shoot a **destroy** shot.
*   **"ENTER":** Shoot a **collect** shot.

### Play

To play the game, run _**space\_invaders.py**_.

To play a different version, change `TASK` to the version you'd like to play in the following code in _**space\_invaders.py**_

```python
def start_game(root, TASK=1)
```
