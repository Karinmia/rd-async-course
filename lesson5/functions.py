def mp_count_words(file_name: str, chunk_start: int, chunk_end: int, counter, lock):
    
    
    _chunk_size = chunk_end - chunk_start
    
    current_progress = 0
    step = _chunk_size / 50
    
    words = {}
    with open(file_name, mode="rb") as f:
        f.seek(chunk_start)
        # gc_disable()
        
        for line in f:
            current_progress += len(line)
            chunk_start += len(line)
            if chunk_start > chunk_end:
                break
            
            _word, _, match_count, _ = line.decode().split("\t")
            if _word in words:
                words[_word] += int(match_count)
            else:
                words[_word] = int(match_count)
                
            # monitoring
            # because of lock, this can slow down processing time
            # if current_progress % step == 0:
            if current_progress >= step:
                with lock:
                    counter.value += current_progress
                
                current_progress = 0
        
        with lock:
            counter.value += current_progress

        # gc_enable()
    
    return words
