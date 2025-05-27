import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#plt.ion()

output_dir = "../output/competitive_pokemon_2022/item_pokemon/"
os.makedirs(output_dir, exist_ok=True)
source = "../dataset/competitive_pokemon_2022/bridge_pokemon_item_USED_WITH_ITEM.csv"

df = pd.read_csv(source, header='infer')
df['Use_Percentage (%)'] = df['Use_Percentage (%)'].str.replace('%', '').astype(float)
top_items = df.groupby('Item')['Use_Percentage (%)'].sum().nlargest(10).index
df_top = df[df['Item'].isin(top_items)]
item_usage = df.groupby('Item')['Use_Percentage (%)'].sum().nlargest(10).reset_index()
item_usage = item_usage.sort_values('Use_Percentage (%)', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=item_usage,
    x='Use_Percentage (%)',
    y='Item',
    palette='viridis'
)
plt.title('Top 10 Ítems Más Usados en Total')
plt.xlabel('Uso total (%)')
plt.ylabel('Ítem')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_10_items_usados.png'))
plt.show()

top3_pokemon_by_item = (
    df_top.groupby('Item')
    .apply(lambda g: g.nlargest(3, 'Use_Percentage (%)'))
    .reset_index(drop=True)
)

plt.figure(figsize=(14, 8))
sns.barplot(
    data=top3_pokemon_by_item,
    x='Use_Percentage (%)',
    y='Pokemon',
    hue='Item',
    dodge=True
)
plt.title('Top Pokémon por cada uno de los 10 ítems más usados')
plt.legend(title='Item', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'top_pokemon_per_item.png'))
plt.show()

#input("Presiona Enter para cerrar las gráficas...")