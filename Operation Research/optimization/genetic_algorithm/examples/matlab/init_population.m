function population = init_population(n_pop, n_bits, min_val, max_val)
population = [];
for i=1:n_pop
    chromo = randi([min_val, max_val], 1, n_bits);
    population = [population; chromo];
end
end