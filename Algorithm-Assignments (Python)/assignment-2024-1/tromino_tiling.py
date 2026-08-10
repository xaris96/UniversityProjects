
def tromino_tiling(n):
    if n < 0:
        grid = "0"
        print("n should be >=0")
        return grid
    #set variables
    G, B, R, X= "G" , "B", "R", "X"
    start = n
    point, z = 0, 0
    #create the grid
    grid = [["O" for _ in range(2**n)] for _ in range(2**n)]
    
    divide(n, grid,point)
    grid = divide(n, grid, point)
    grid[3][3] = X
    for row in grid:
        print(' '.join(row))
    return grid
def divide(n, grid,point):
    G, B, R, X= "G" , "B", "R", "X"
    colour = [B , R]
    z = 0
    hsize = 2**n//2
    if n == 0:
        grid = "X"
        return grid
    elif n == 1:
        grid = [[G , "X"], [G, G]]
        return grid
    elif n == 2:
        if point == 0: #topleft
            grid[hsize - 1][hsize - 1] = G
            grid[hsize][hsize-1] = G
            grid[hsize-1][hsize] = G
        elif point == 1: #topright
            grid[hsize][hsize] = G
            grid[hsize - 1][hsize] = G
            grid[hsize-1][hsize-1] = G
        elif point == 2: #botleft
            grid[hsize][hsize] = G
            grid[hsize][hsize -1] = G
            grid[hsize-1][hsize-1] = G
        elif point == 3: #botright
            grid[hsize][hsize] = G
            grid[hsize-1][hsize] = G
            grid[hsize][hsize-1] = G
        w = 0
        for i in range (len(grid)):
            for j in range (len(grid)):
                if i >= 2 and w == 0:
                    colour.reverse()
                    w = 1
                if grid[i][j] != G:
                    grid[i][j] = colour[(z // 2) % 2]
                z += 1
        colour.reverse()
        return grid
    elif n > 2:
        if point == 0 or point == 3:
            grid[hsize][hsize] = G
            grid[hsize-1][hsize] = G
            grid[hsize][hsize-1] = G
        elif point == 1:
            grid[hsize][hsize] = G
            grid[hsize - 1][hsize] = G
            grid[hsize-1][hsize-1] = G
        elif point == 2:
            grid[hsize][hsize] = G
            grid[hsize][hsize -1] = G
            grid[hsize-1][hsize-1] = G
        bl = [row[:hsize] for row in grid[hsize:]]
        br = [row[hsize : ] for row in grid[hsize:]]
        tr = [row[hsize : ] for row in grid[: hsize]]
        tl = [row[: hsize  ] for row in grid[: hsize]]
        n = n - 1
        point = 0
        for subgrid in (tl, tr, bl, br):
            subgrid = divide(n, subgrid, point)
            point += 1
        left = tl + bl
        right = tr + br
        for i in range(len(left)):
            grid[i] = left[i] + right[i]
    return grid

import argparse
parsing = argparse.ArgumentParser(description = 'creating a tromino tiling')
parsing.add_argument('n', type = int, help = 'n should be a positive integer')
args = parsing.parse_args()
n = args.n

tromino_tiling(n)

