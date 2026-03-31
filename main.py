import sys

def wlcs(s1: str, s2: str, weights: dict[str, int]) -> tuple[int, str]:
    m = len(s1)
    n = len(s2)
    
    dp = [[(0, "") for _ in range(n+1)] for _ in range(m+1)]
    
    for i in range(1,m+1):
        for j in range(1,n+1):
            if s1[i-1] == s2[j -1]:
                prev_value, prev_str = dp[i - 1][j - 1]
                dp[i][j] = (prev_value +weights[s1[i - 1]], prev_str+s1[i-1])
            else:
                val1, str1 = dp[i-1][j]
                val2, str2 = dp[i][j-1]
                
                if val1 >= val2:
                    dp[i][j] = (val1,str1)
                else:
                    dp[i][j] = (val2,str2)
    
    return dp[m][n]


def main():
    data = sys.stdin.read().strip().split('\n')
    K = int(data[0].strip())
    
    weights = {}
    line_idx = 1
    for _ in range(K):
        parts = data[line_idx].split()
        char = parts[0]
        value = int(parts[1])
        weights[char] = value
        line_idx += 1
    
    A = data[line_idx].strip()
    line_idx += 1
    
    B = data[line_idx].strip()
    value, subsequence = wlcs(A, B, weights)
    
    print(value)
    print(subsequence)


if __name__ == "__main__":
    main()
