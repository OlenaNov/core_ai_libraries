from utils import *

# TODO with The Best Practice of Coding
# Te last for - a cosa serve??

def chunk_characters(text, size, overlap=0):
    step = size - overlap
    result = []

    for i in range(0, len(text), step):
        segment = text[i:i + size] 
        if segment.strip():
            result.append(segment)
    return result

for ov in (0, 20):
    c = chunk_characters(TEXT, 100, ov)
    print(ov, len(c), [len(x) for x in c])

c = chunk_characters(TEXT, 100, 20)
print(repr(c[0][-20:]))
print(repr(c[1][:20]))