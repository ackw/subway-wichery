% ---------------------------------------------------------------------------------------------
% INIT
% ---------------------------------------------------------------------------------------------
% for appending options into a list
append([], Y, Y).
append([H|X], Y, [H|Z]):-
    append(X, Y, Z).

% ---------------------------------------------------------------------------------------------
% LOGIC
% ---------------------------------------------------------------------------------------------
% for ensuring that meals are correct
healthy_meal(healthy).
value_meal(value).
vegan_meal(vegan).
veg_meal(meat_free).
gluten_free_meal(gluten_free).

% display default list of options
default_options(Opt, X):-
    Opt == meals -> meals(X);
    Opt == breads -> breads(X);
    Opt == mains -> mains(X);
    Opt == veggies -> veggies(X);
    Opt == sauces -> sauces(X);
    Opt == topups -> topups(X);
    Opt == sides -> sides(X);
    Opt == drinks -> drinks(X).

% display available options based on selected meal
available_options(Opt, X):-
    Opt == meals -> display_meals(X);
    Opt == breads -> display_breads(X);
    Opt == mains -> display_mains(X);
    Opt == veggies -> display_veggies(X);
    Opt == sauces -> display_sauces(X);
    Opt == topups -> display_topups(X);
    Opt == sides -> display_sides(X);
    Opt == drinks -> display_drinks(X).

% display list of final selection
chosen_options(Opt, X):-
    Opt == meals -> findall(X, chosen_meals(X), X);
    Opt == breads -> findall(X, chosen_breads(X), X);
    Opt == mains -> findall(X, chosen_mains(X), X);
    Opt == veggies -> findall(X, chosen_veggies(X), X);
    Opt == sauces -> findall(X, chosen_sauces(X), X);
    Opt == topups -> findall(X, chosen_topups(X), X);
    Opt == sides -> findall(X, chosen_sides(X), X);
    Opt == drinks -> findall(X, chosen_drinks(X), X).

% ---------------------------------------------------------------------------------------------
% THE MENU
% ---------------------------------------------------------------------------------------------
meals([regular, healthy, value, vegan, meat_free, gluten_free]).
reg_breads([parmesan_oregano, honey_oat]).
vegan_breads([italian_wheat, hearty_italian, multigrain, flatbread, tortilla]).

reg_mains([cold_cut_trio, tuna, egg_mayo, steak, chicken_breast, blt, meatballs]).
veg_mains([mushroom_galore, veggie_patty]).

veggies([cucumber, capsicum, lettuce, onions, tomatoes, olives, jalapenos, pickles]).
reg_sauces([chipotle_southwest, bbq, ranch, mayonnaise, mustard]).
lf_sauces([honey_mustard, sweet_onion, ketchup]).

reg_topups([mozerella_cheese, cheddar_cheese, egg_mayo]).
vegan_topups([avocado, mushrooms]).

reg_sides([chips, cookie]).
lf_sides([banana, granola_bar, mushroom_soup, tomato_soup]).

reg_drinks([soda]).
lf_drinks([bottled_water, orange_juice, green_tea, black_tea, americano]).

% ---------------------------------------------------------------------------------------------
% MERGE & DISPLAY MENU
% ---------------------------------------------------------------------------------------------
breads(X):- vegan_breads(A1), reg_breads(A2), append(A1, A2, X).
mains(X):- veg_mains(B1), reg_mains(B2), append(B1, B2, X).
sauces(X):- lf_sauces(C1), reg_sauces(C2), append(C1, C2, X).
topups(X):- vegan_topups(D1), reg_topups(D2), append(D1, D2, X).
sides(X):- lf_sides(E1), reg_sides(E2), append(E1, E2, X).
drinks(X):- lf_drinks(F1), reg_drinks(F2), append(F1, F2, X).

% ---------------------------------------------------------------------------------------------
% DISPLAY LISTS BASED ON MEAL
% ---------------------------------------------------------------------------------------------
display_meals(X):- meals(X).

display_breads(X):-
    chosen_meals(Y), vegan_meal(Y) -> vegan_breads(X);
    chosen_meals(Y), \+ gluten_free_meal(Y), breads(X).

display_mains(X):-
    chosen_meals(Y), vegan_meal(Y) -> veg_mains(X);
    chosen_meals(Y), veg_meal(Y) -> veg_mains(X);
    chosen_meals(Y), value_meal(Y) -> reg_mains(X);
    mains(X).

display_veggies(X):- veggies(X).

display_sauces(X):-
    chosen_meals(Y), healthy_meal(Y) -> lf_sauces(X);
    sauces(X).

display_topups(X):-
    chosen_meals(Y), vegan_meal(Y) -> vegan_topups(X);
    chosen_meals(Y), \+ value_meal(Y), topups(X).

display_sides(X):-
    chosen_meals(Y), healthy_meal(Y) -> lf_sides(X);
    chosen_meals(Y), gluten_free_meal(Y) -> lf_sides(X);
    sides(X).

display_drinks(X):-
    chosen_meals(Y), healthy_meal(Y) -> lf_drinks(X);
    drinks(X).