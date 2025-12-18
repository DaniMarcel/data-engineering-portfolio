"""Hadoop MapReduce Word Count Example"""

# Mapper
def mapper(line):
    """Emit word, count pairs"""
    for word in line.strip().split():
        print(f"{word}\t1")

# Reducer
def reducer(word, counts):
    """Sum counts for each word"""
    total = sum(int(c) for c in counts)
    print(f"{word}\t{total}")

# Simulate MapReduce
if __name__ == '__main__':
    # Sample data
    data = [
        "hello world",
        "hello hadoop",
        "world of big data"
    ]
    
    print("MAP PHASE:")
    print("-" * 40)
    for line in data:
        mapper(line)
    
    print("\nREDUCE PHASE:")
    print("-" * 40)
    # Simulated reduce (in real Hadoop this happens distributed)
    word_counts = {}
    for line in data:
        for word in line.strip().split():
            word_counts[word] = word_counts.get(word, 0) + 1
    
    for word, count in sorted(word_counts.items()):
        print(f"{word}\t{count}")
    
    print("\n✅ MapReduce simulation completed!")
