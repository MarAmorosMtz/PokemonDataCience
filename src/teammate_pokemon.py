import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#plt.ion()

output_dir = "../output/competitive_pokemon_2022/teammate_pokemon/"
os.makedirs(output_dir, exist_ok=True)
source = "../dataset/competitive_pokemon_2022/bridge_pokemon_pokemon_USED_IN_TEAM_WITH.csv"

df = pd.read_csv(source, header='infer')
df['Use_Percentage (%)'] = df['Use_Percentage (%)'].str.replace('%', '').astype(float)

top_pokemons = df.groupby('Pokemon')['Use_Percentage (%)'].sum().nlargest(10).index
df_top = df[df['Pokemon'].isin(top_pokemons)]

pokemon_usage = df.groupby('Pokemon')['Use_Percentage (%)'].sum().nlargest(10).reset_index()
pokemon_usage = pokemon_usage.sort_values('Use_Percentage (%)', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=pokemon_usage,
    x='Use_Percentage (%)',
    y='Pokemon',
    palette='viridis'
)
plt.title('Top 10 Pokemons mas usados en Total')
plt.xlabel('Uso total (%)')
plt.ylabel('Pokemon')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_10_pokemons_usados.png'))
plt.show()

top3_teammate_by_pokemon = (
    df_top.groupby('Pokemon')
    .apply(lambda g: g.nlargest(3, 'Use_Percentage (%)'))
    .reset_index(drop=True)
)

plt.figure(figsize=(14, 10))
sns.barplot(
    data=top3_teammate_by_pokemon,
    x='Use_Percentage (%)',
    y='Teammate',
    hue='Pokemon',
    dodge=True
)
plt.title('Top Pokémon usado en equipo con los 10 Pokemones mas usados')
plt.legend(title='Pokemon', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_teammate_per_pokemon.png'))
plt.show()

#input("Presiona Enter para cerrar las gráficas...")