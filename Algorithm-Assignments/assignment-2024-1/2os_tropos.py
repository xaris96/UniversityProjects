def tromino(n):
    if n < 0:
        grid = "0"
        print("n should be >=0")
        return grid
    #set variables
    G, B, R, X= "G" , "B", "R", "X"
    start = n
    z = 0
    #create the grid
    grid = [["O" for _ in range(2**n)] for _ in range(2**n)]
    # inside_tr function will fill the grid
    topleft = [[B, B, R, R], [B, G, G, R], [R, G, B, B], [R, R, B, G]]
    topright = [[B, B, R, R], [B, G, G, R], [R, R, G, B], [G, R, B, B]]
    botleft = [[B, B, R, G], [B, G, R, R], [R, G, G, B], [R, R, B, B]]
    botright = [[G, B, R, R], [B, B, G, R], [R, G, G, B], [R, R, B, B]]
    def divide(n, grid, z):
        if n == 0:
            grid = "X"
            return grid
        elif n == 1:
            grid = [[G , "X"], [G, G]]
            return grid
        elif n == 2:
            hsize = 2**n//2
            if z == 0 or z == 1:
                grid = topleft
                grid[hsize - 1][hsize - 1] = G
                grid[hsize][hsize-1] = G
                grid[hsize-1][hsize] = G
                if z == 0:
                    grid[3][3] = X
            elif z == 2:
                grid = topright
                grid[hsize][hsize] = G
                grid[hsize - 1][hsize] = G
                grid[hsize-1][hsize-1] = G
            elif z == 3:
                grid = botleft
                grid[hsize][hsize] = G
                grid[hsize][hsize -1] = G
                grid[hsize-1][hsize-1] = G
            elif z == 4:
                grid = botright
                grid[hsize][hsize] = G
                grid[hsize-1][hsize] = G
                grid[hsize][hsize-1] = G
            return grid
        elif n > 2:
            z = 1
            hsize = 2**n//2
            grid[hsize][hsize] = G
            grid[hsize][hsize-1] = G
            grid[hsize-1][hsize] = G
            bl = [row[:hsize] for row in grid[hsize:]]
            br = [row[hsize : ] for row in grid[hsize:]]
            tr = [row[hsize : ] for row in grid[: hsize]]
            tl = [row[: hsize  ] for row in grid[: hsize]]
            n = n - 1
            tl = divide(n, tl, z)
            z = z + 1
            tr = divide(n, tr, z)
            z = z + 1
            bl= divide(n, bl, z)
            z = z + 1
            br = divide(n, br, z)
            z = z + 1
            left = tl + bl
            right = tr + br
            for i in range(len(left)):
                grid[i] = left[i] + right[i]
            return grid
    grid = divide(n, grid, z)
    colour2 = [R , G]
    colour1 = [B, G]
    x = 1
    y = 0
    onetime = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if i + j == len(grid) - 1:
                if i < j:
                    grid[i][j] = colour2[y]
                else :
                    grid[i][j] = colour2[(y+1) % 2]
                y = (y+1) % 2
            if i == j:
                if onetime < 4:
                    grid[i][j] = colour1[(x+1)%2]
                    onetime += 1
                else:
                    grid[i][j] = colour1[x]
                x = (x+1) % 2
    grid[3][3] = X
    for row in grid:
        print(' '.join(row))
    return grid
grid = tromino(5)

