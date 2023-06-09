%%
% GA parameters
n_pop  = 10;
n_gen  = 50;
min_val= 0 ;
max_val= 10;

% Linear equation paramters

A= [1 2 3 4];
b= 30;

population = init_population(n_pop, length(A), min_val, max_val );


%%


for i=1:n_gen
    
   disp(i)
end


%