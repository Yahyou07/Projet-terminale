from PIL import Image
import random
#Petit programme qui permet d'extraire les images d'un gif
'''
# Ouvrir le GIF
gif = Image.open("Objects/fumee.gif")


# Extraire chaque frame
for i in range(gif.n_frames):
    gif.seek(i)  # Aller à la frame i
    gif.save(f"Objects/frame_{i}.png")  # Sauvegarder l'image

print("Extraction terminée !")

'''

def generate_tree_positions(max_x, max_y, num_trees, min_distance, max_attempts=1000):
    positions = []
    for _ in range(num_trees):
        attempt = 0
        while attempt < max_attempts:
            pos = (random.randint(0, max_x), random.randint(0, max_y))
            if all(abs(pos[0] - x) > min_distance and abs(pos[1] - y) > min_distance for x, y in positions):
                positions.append(pos)
                break
            attempt += 1
        else:
            print(f"Could not place tree {len(positions) + 1} after {max_attempts} attempts.")
    return positions

# Generate positions for 30 trees with a minimum distance of 100 pixels
tree_positions = generate_tree_positions(1560, 1530, 30, 80)
print(tree_positions)