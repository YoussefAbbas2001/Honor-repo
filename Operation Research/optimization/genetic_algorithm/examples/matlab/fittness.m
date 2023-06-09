function fit = fittness(chromo, A, b)

    LHS = A(1)*chromo(1) + A(2)*chromo(2) + A(3)*chromo(3) + A(4)*chromo(4);
    fit = abs(b - LHS);

end