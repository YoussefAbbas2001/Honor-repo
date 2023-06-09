function mutated = mutation(population, p_mutation)
    mutated = [];
    for i=1:length(population)
        mutated =  [mutated ; population(i,:)];
        if rand() > p_mutation
            % mutation p_mutation % of the population chromosomes
            val = randi([0 30]);
            pos = randi([1 length(length(population))]);
            mutated(i, pos) = val;
            
        end
    end
end