n = int(input())

segs = ["123567", "36", "13457", "13467", "2346",
        "12467", "124567", "136", "1234567", "123467"]

ans = 1
for _ in range(n):
    s = input().strip()

    
    work = set()
    for i in range(7):
        if s[i] == '1':
            work.add(str(i + 1))

   
    seen = {}
    views = []
    for d in segs:
        v = frozenset(set(d) & work)
        views.append(v)
        seen[v] = seen.get(v, 0) + 1

  
    unique = 0
    for v in views:
        if seen[v] == 1:
            unique += 1

    ans *= unique

print(ans)