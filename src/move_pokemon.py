import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#plt.ion()

output_dir = "../output/competitive_pokemon_2022/move_pokemon/"
os.makedirs(output_dir, exist_ok=True)
source = "../dataset/competitive_pokemon_2022/bridge_pokemon_move_USED_WITH_MOVE.csv"

df = pd.read_csv(source, header='infer')
df['Use_Percentage (%)'] = df['Use_Percentage (%)'].str.replace('%', '').astype(float)
top_moves = df.groupby('Move')['Use_Percentage (%)'].sum().nlargest(10).index
df_top = df[df['Move'].isin(top_moves)]
moves_usage = df.groupby('Move')['Use_Percentage (%)'].sum().nlargest(10).reset_index()
moves_usage = moves_usage.sort_values('Use_Percentage (%)', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=moves_usage,
    x='Use_Percentage (%)',
    y='Move',
    palette='viridis'
)
plt.title('Top 10 Movimientos Más Usados en Total')
plt.xlabel('Uso total (%)')
plt.ylabel('Movimiento')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_10_items_usados.png'))
plt.show()

top3_pokemon_by_movement = (
    df_top.groupby('Move')
    .apply(lambda g: g.nlargest(3, 'Use_Percentage (%)'))
    .reset_index(drop=True)
)

plt.figure(figsize=(14, 10))
sns.barplot(
    data=top3_pokemon_by_movement,
    x='Use_Percentage (%)',
    y='Pokemon',
    hue='Move',
    dodge=True
)
plt.title('Top Pokémon por cada uno de los 10 movimientos más usados')
plt.legend(title='Movement', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_pokemon_per_item.png'))
plt.show()

#input("Presiona Enter para cerrar las gráficas...")