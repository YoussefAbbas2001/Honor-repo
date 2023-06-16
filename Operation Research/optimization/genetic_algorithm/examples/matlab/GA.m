
%% CONSTANTS OF PROBLEM
n_genes       = 4;                % number of parameters
n_chromosomes = 6;                % number of chromosomes in each generation
n_generations = 50;               % maximum number of iteration
min_val       = 0 ;               % minimum value of variable
max_val       = 30;               % maximum value of variable 
mutation_rate = 0.1;              % Mutation percentage.
crossover_rate = 0.8;             % Crossover percentage.

coeff         = [1 2 3 4];        % coeff of linear equation
solutions     = [];               % matrix of fitted solutions


%% INITIALIZATION 
    
% Initialization (random from 0 to 30)
chromosome = randi([min_val max_val] , n_genes , n_chromosomes);
for i = 1:n_chromosomes
    loss(i) = abs(coeff(1)*chromosome(1,i) + coeff(2)*chromosome(2,i) + coeff(3)*chromosome(3,i) + coeff(4)*chromosome(4,i) - 30);
end

%% EVOLUTION
for iteration = 1:n_generations
%% Calculate fitness
    for i = 1:n_chromosomes
        fitness(i) = 1/(1+loss(i));
    end
    total_fitness = sum(fitness);

%% Calculate probability of each chromosome
    for i = 1:n_chromosomes
        pdf(i) = fitness(i)/total_fitness;
    end

    % Cumulative probability values
    cdf(1) = prob(1);
    for i = 2:n_chromosomes
        cdf(i) = cdf(i-1) + pdf(i);
    end

    %% Roulette wheel selection
    % Initialize selection numbers (random from 0 to 1)
    R = rand(n_chromosomes,1);

    for i = 1:n_chromosomes
       j = 1;
       while(R(i) > C(j))
           j = j+1;
       end
       new_chromosome(:, i) = chromosome(:, j);
    end
    chromosome = new_chromosome;

    %% Crossover

    % Randomly initialized (from 0 to 1)
    R = rand(n_chromosomes,1);

    % Parents selection
    k = 1;
    for i = 1:n_chromosomes
        if(R(i) < crossover_rate)
            parent(:, k) = chromosome(:, i);
            parent_index(k) = i;
            k = k+1;
        end
    end
    % Repeat first element in the end of the array (helps in crossover phase)
    parent(:, k) = chromosome(:, parent_index(1));
    parent_index(k) = parent_index(1);

    % Random numbers from 2 to n_genes
    crossover_point = randi([2 n_genes] , 1 , length(parent_index)-1);

    for i = 1:k-1
        parent(crossover_point(i):end , i) = chromosome(crossover_point(i):end , parent_index(i+1));
    end

    % Use parents to update chromosomes
    for i = 1:k-1
        chromosome(: ,parent_index(i)) = parent(:, i);
    end

    %% Mutation

    if rand() > mutation_rate
        % replaced by a random number between min_val-max_val
        chromosome(gen_position(1)) = randi([min_val max_val] , 1 , 1);

    end
    
    %% Calculate objective fn of new chromosomes
    for i = 1:n_chromosomes
        loss(i) = abs(chromosome(1,i) + 2*chromosome(2,i) + 3*chromosome(3,i) + 4*chromosome(4,i) - 30);
        if loss(i) == 0
            % Check that solution satisfy equation
            solutions = [solutions  chromosome(:,i)];
            
            
            % Remove duplicated
            solutions = unique(solutions', 'rows')';
            
            
            fprintf('gen:(%d)  soln-> 1 * (%d) + 2 * (%d) + 3 * (%d) + 4 * (%d) \n',iteration,chromosome(1,i),chromosome(2,i),chromosome(3,i), chromosome(4,i))
        end
    end

end


solutions
