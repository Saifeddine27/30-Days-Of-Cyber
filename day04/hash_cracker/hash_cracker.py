import hashlib
import time
import itertools
from multiprocessing import Process, Value, Manager, cpu_count

def detect_hash(target_hash: str) -> str:
    n = len(target_hash)
    if n == 32: return "md5"
    elif n == 40: return "sha1"
    elif n == 64: return "sha256"
    elif n == 128: return "sha512"
    else: return "UNKNOWN"

def hash_word(word: str, hash_type: str) -> str:
    if hash_type == "md5": return hashlib.md5(word.encode()).hexdigest()
    elif hash_type == "sha1": return hashlib.sha1(word.encode()).hexdigest()
    elif hash_type == "sha256": return hashlib.sha256(word.encode()).hexdigest()
    elif hash_type == "sha512": return hashlib.sha512(word.encode()).hexdigest()
    else: return "UNKNOWN"

def dict_cracker(hash_target: str, hash_type: str, dict_path: str) -> str:
    attempts = 0
    start_time = time.time()
    
    with open(dict_path, 'r', encoding='latin-1') as f:
        for word in f:
            word2hash = word.strip()
            attempts += 1
            if hash_word(word2hash, hash_type) == hash_target:
                time_passed = time.time() - start_time
                speed = attempts / time_passed if time_passed > 0 else 0
                print(f"Tried {attempts} words in {time_passed:.2f}s with a speed of {speed:.0f} hashes/s")
                return word2hash
                
    time_passed = time.time() - start_time
    speed = attempts / time_passed if time_passed > 0 else 0
    print(f"Tried {attempts} words in {time_passed:.2f}s with a speed of {speed:.0f} hashes/s")
    return None

def brute_force_cracker(hash_target: str, hash_type: str, max_length: int, charset: str) -> str:
    attempts = 0
    start_time = time.time()
    
    for length in range(1, max_length + 1):
        for word in itertools.product(charset, repeat=length):
            attempts += 1
            word2hash = "".join(word)
            if hash_word(word2hash, hash_type) == hash_target:
                time_passed = time.time() - start_time
                speed = attempts / time_passed if time_passed > 0 else 0
                print(f"Tried {attempts} words in {time_passed:.2f}s with a speed of {speed:.0f} hashes/s")
                return word2hash
                
    time_passed = time.time() - start_time
    speed = attempts / time_passed if time_passed > 0 else 0
    print(f"Tried {attempts} words in {time_passed:.2f}s with a speed of {speed:.0f} hashes/s")
    return None

def generate_mutations(word):
    mutations = []
    mutations.append(word.capitalize())        
    mutations.append(word.upper())            
    mutations.append(word[::-1])               
    for i in range(10):
        mutations.append(word + str(i))        
    leet = word.replace('a', '@').replace('e', '3').replace('o', '0').replace('s', '$').replace('i', '1')
    mutations.append(leet)
    return mutations

def crack_rules(target_hash, hash_type, wordlist_path):
    attempts = 0
    start_time = time.time()
    
    with open(wordlist_path, 'r', encoding='latin-1') as f:
        for line in f:
            word = line.strip()
            attempts += 1
            if hash_word(word, hash_type) == target_hash:
                elapsed = time.time() - start_time
                speed = attempts / elapsed if elapsed > 0 else 0
                print(f"  Tried {attempts} words in {elapsed:.2f}s ({speed:.0f} hashes/sec)")
                return word
                
            for mutation in generate_mutations(word):
                attempts += 1
                if hash_word(mutation, hash_type) == target_hash:
                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0
                    print(f"  Tried {attempts} words in {elapsed:.2f}s ({speed:.0f} hashes/sec)")
                    return mutation
                    
    elapsed = time.time() - start_time
    speed = attempts / elapsed if elapsed > 0 else 0
    print(f"  Tried {attempts} words in {elapsed:.2f}s ({speed:.0f} hashes/sec)")
    return None

def list_cracker(word_list, target_hash, hash_type, ind_found, result):
    for word in word_list:
        if ind_found.value == 1:
            return
        if hash_word(word, hash_type) == target_hash:
            ind_found.value = 1
            result.append(word)
            return

def dict_multiprocessing_cracker(hash_target: str, hash_type: str, dict_path: str):
    with open(dict_path, 'r', encoding='latin-1') as f:
        words = [word.strip() for word in f]

    num_cores = cpu_count()
    list_size = len(words) // num_cores
    lists = []
    
    for i in range(num_cores):
        list_start = i * list_size
        list_end = list_start + list_size if i < num_cores - 1 else len(words)
        lists.append(words[list_start:list_end]) 
        
    ind_found = Value("i", 0)
    manager = Manager()
    results = manager.list()
    processes = []

    for lista in lists:
        p = Process(target=list_cracker, args=(lista, hash_target, hash_type, ind_found, results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    if results:
        return results[0]

    return None