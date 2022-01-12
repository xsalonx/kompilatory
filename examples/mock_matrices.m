A = zeros(3, 3, 3);
print A;
G = [[1, 2],[2, 3]];
H = [[1, 2],[4, 3]];
B = -(G .+ H);
print B;
print G;
G[0, 0] = 100;
print G;