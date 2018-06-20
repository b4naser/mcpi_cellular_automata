import mcpi.minecraft
import mcpi.block

from time import sleep, time
import math
import sys
import random
import copy

# If less cell dies
ALIVE_CELL_LIMIT = 12
# If more cell become alive
DEAD_CELL_LIMIT = 8

def generateBlocks(mode):
    blocks = set()

    if mode == 1:
        # Cube 5x5x5
        for x in range(-2, 3):
            for y in range(18, 23):
                for z in range(-2, 3):
                    blocks.add((x, y, z))
    elif mode == 2:
        # Filled sphere
        for x in range(-5, 6):
            for y in range(15, 26):
                for z in range(-5, 6):
                    if math.sqrt(x**2 + (y-20)**2 + z**2) < 3:
                        blocks.add((x, y, z))
    elif mode == 3:
        # Cube 10x10x10 with empty sphere inside
        for x in range(-5, 6):
            for y in range(15, 26):
                for z in range(-5, 6):
                    if math.sqrt(x**2 + (y-20)**2 + z**2) > 5:
                        blocks.add((x, y, z))

    return blocks

def getALiveNeighboursCount(block, blocks):
    count = 0

    for b in blocks:
        if block == b:
            continue

        x_cond = abs(b[0] - block[0]) <= 1
        if not x_cond:
            continue

        y_cond = abs(b[1] - block[1]) <= 1
        if not y_cond:
            continue

        z_cond = abs(b[2] - block[2]) <= 1
        if not z_cond:
            continue

        count += 1
    
    return count

if __name__ == "__main__":       
    mc = mcpi.minecraft.Minecraft.create()
    
    playerPos = mc.player.getPos()
    mc.player.setPos(10, 20, 10)

    mc.postToChat("Cellular automata started")

    mc.setBlocks(-20, 0, -20, 20, 40, 20, mcpi.block.AIR.id)

    blocks = generateBlocks(3)

    for block in blocks:
        mc.setBlock(block[0], block[1], block[2], mcpi.block.WOOL.id, int(getALiveNeighboursCount(block, blocks)/2))
    
    sleep(1)

    while 1:
        surroundBlocks = set()
        diedBlocks = set()
        newAliveBlocks = set()

        for block in blocks:
            for x in range(block[0]-1, block[0]+2):
                for y in range(block[1]-1, block[1]+2):
                    for z in range(block[2]-1, block[2]+2):
                        surroundBlocks.add((x, y, z))
        
        surroundBlocks = surroundBlocks - blocks

        for block in blocks:
            if getALiveNeighboursCount(block, blocks) < ALIVE_CELL_LIMIT:
                diedBlocks.add(block)
  

        for block in surroundBlocks:
            if getALiveNeighboursCount(block, blocks) > DEAD_CELL_LIMIT:
                newAliveBlocks.add(block)
                          
        for block in diedBlocks:
            mc.setBlock(block[0], block[1], block[2], 0)

        for block in newAliveBlocks:
             mc.setBlock(block[0], block[1], block[2], mcpi.block.WOOL.id, int(getALiveNeighboursCount(block, blocks)/2)) 
        
        blocks = (blocks - diedBlocks) | newAliveBlocks
               
        if len(blocks) > 2000:
            mc.postToChat("Max. block reached")
            break
        elif len(blocks) == 0:
            mc.postToChat("All cells died")