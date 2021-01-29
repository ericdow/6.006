import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):

        # Compute the energy of the first row
        dp = [[0 for x in range(self.height)] for y in range(self.width)]
        for i in range(self.width):
            dp[i][0] = self.energy(i,0)

        # Allocate parent indices
        parent = [[0 for x in range(self.height)] for y in range(self.width)]

        # Solve the dp from the first row down
        for j in range(1,self.height):
            for i in range(self.width):
                e_ij = self.energy(i,j)
                min_dp_jm1 = dp[i][j-1]
                parent_tmp = i
                    
                if i > 0:
                    if dp[i-1][j-1] < min_dp_jm1:
                        parent_tmp = i-1
                        min_dp_jm1 = dp[i-1][j-1]

                if i < self.width-1:
                    if dp[i+1][j-1] < min_dp_jm1:
                        min_dp_jm1 = dp[i+1][j-1]
                        parent_tmp = i+1

                dp[i][j] = min_dp_jm1 + e_ij
                parent[i][j] = parent_tmp

        # Find the column with the lowest energy
        i_min = 0
        dp_min = dp[0][self.height-1]
        for i in range(1,self.width):
            if (dp[i][self.height-1] < dp_min):
                i_min = i
                dp_min = dp[i][self.height-1]

        # Trace back to find optimal path
        path = [(i_min,self.height-1)]
        i_curr = i_min
        for j in reversed(range(1,self.height)):
            i_curr = parent[i_curr][j]
            path.append((i_curr,j-1))

        path.reverse()

        return path

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
