'''
    1. Load del dataset
    2. Normalizzazione del dataset
    3. Lettura dati dell'utente
        3a. Normalizzazione dei dati risp. al dataset
    4. Calcolo dei vicini:
        4a. calcolo distanze
        4b. Ordinamento in base alle K distanze minori
        4c. Retrieve dei risultati
    5. Stampa dei risultati

'''



import csv
columns = []
pokemon_dataset = []
with open('pokemon.csv') as file:
    print(type(file))
    reader = csv.reader(file)
    columns = next(reader)
    for row in reader:
        pokemon_dataset.append(row)


for i in pokemon_dataset:
    print(f"{i[0]} - {i[1]} (gen. {i[11]})")

for k, v in zip(columns, pokemon_dataset[0]):
    print(f"{k:10} -> {v:15} ({type(v)})")


# Colonne con valori che dobbiamo trasformare in valori numerici
num_indexes = [5, 6, 7, 8, 9, 10]

numerical_data = []
for i in range(len(pokemon_dataset)):
    row = pokemon_dataset[i]
    num_row = []
    for col in num_indexes:
        num_row.append(float(row[col]))

    numerical_data.append(num_row)

for k, v in zip(columns[5:11], numerical_data[0]):
    print(f"{k:10} -> {v:15} ({type(v)})")

'''
Normalizzare significa scalare tutti i dati fra 0 e 1.
Prendiamo la prima entry del dataset e riga per riga/colonna per colonna
ci andiamo a costruire un elenco di valori per colonna:
es. dataset di partenza:
    [
        [20, 40, 50],
        [30, 10, 60],
        [50, 35, 70],
        [10, 11, 80],
    ]

    col_values:
        [ 20, 30, 50, 10 ],
        [ 40, 10, 35, 11 ],
        [ 50, 60, 70, 80 ]
    trovo min e max delle singole righe di col_values (i cui indici sono 
    gli indici delle colonne del dataset iniziale )

    colonna 0 -> (10, 50)
    colonna 1 -> (10, 40)
    colonna 2 -> (50, 80)

    quindi avremo: 
    [
        (10, 50),
        (10, 40),
        (50, 80),
    ]
'''


def get_min_max(dataset):
    min_max = []

    for i in range(len(dataset[0])):
        # per ciascuna colonna:
            # prendiamo tutti i valori di quella colonna nel dataset
            # calcoliamo val. minimo e max della colonna
            # add della tupla min/max della colonna alla lista min_max
        col_values = [row[i] for row in dataset]
        min_max.append((min(col_values), max(col_values)))

    return min_max
def normalize(dataset):
    output = []

    min_max = get_min_max(dataset)    

    for row in dataset:
        scaled_row = []
        for col_index in range(len(row)):
            col_value = row[col_index]
            scaled_value = (col_value - min_max[col_index][0])/(min_max[col_index][1] - min_max[col_index][0])
            scaled_row.append(scaled_value)

        output.append(scaled_row)

    return output

# Calcola la distanza di minkowski fra 2 punti. 
# Si può semplificare andando a prendere direttamente la dist. euclidea e basta
def minkowski_distance(p1, p2, p = 2):
        # https://rittikghosh.com/images/min.png
        # p = 1 -> Manhattan Distance
        # p = 2 -> Euclidean Distance
        dim = len(p1)
        distance = 0
        for d in range(dim):
            distance += abs(p1[d] - p2[d]) ** p

        distance = distance**(1/p)

        return distance

'''
    Questa funzione ci restituisce una lista di lunghezza pari a K 
    contenente una serie di tuple in cui abbiamo:
        - indice i dell'elemento nel dataset
        - distanza della riga test_row dall'elemento con indice i
'''
def get_k_neighbors(k, dataset, test_row):
    dataset.append(test_row)
    norm_dataset = normalize(dataset)
    norm_test_row = norm_dataset[-1]
    norm_dataset = norm_dataset[:-1]

    distances = []

    for i in range(len(norm_dataset)):
        row = norm_dataset[i]
        d = minkowski_distance(norm_test_row, row)
        distances.append((i, d))


    distances.sort(key=lambda tup: tup[1])

    return distances[:k]

def print_pokemon_info(i):
    s = f"{pokemon_dataset[i][0]} - {pokemon_dataset[i][1]}, di tipo {pokemon_dataset[i][2]} (gen. {pokemon_dataset[i][-2]})"
    if pokemon_dataset[i][-1] == "True":
        s += f"\n - POKEMON LEGGENDARIO"

    for k in num_indexes:
        s += f"\n{columns[k]:20}: {pokemon_dataset[i][k]}"
    return s


user_row = []

for i in range(len(num_indexes)):
    col_index = num_indexes[i]
    v = input(f"Inserisci il tuo valore di {columns[col_index]}\n")
    user_row.append(float(v))

for k, v in zip(columns[5:11], user_row):
    print(f"{k:10} -> {v:15} ({type(v)})")

print("Calcolo i tuoi pokemon più affini...")

l = get_k_neighbors(5, numerical_data, user_row)
print(l)

for p in l:
    print(print_pokemon_info(p[0]))

