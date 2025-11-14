import random


def shuffle(array):
    for i in range(len(array) - 1, 0, -1):
        j = random.randint(0, i)
        array[i], array[j] = array[j], array[i]
            
if __name__ == "__main__":
    N = 10 
    num_shuffles = 1000  
    
    counts = [[0] * N for _ in range(N)]
    
    for _ in range(num_shuffles):
        a = list(range(1, N + 1))
        shuffle(a)  
        for pos, num in enumerate(a):
            counts[num - 1][pos] += 1  
    
    
    print(f"После {num_shuffles} тасовок:" )
    print("Порядок:      " + "  ".join(f"num {i+1}" for i in range(N)))
    for i in range(N):
        print(f"Число {i+1:2}:", "  ".join(f"{counts[i][pos]:3}" for pos in range(N)))
