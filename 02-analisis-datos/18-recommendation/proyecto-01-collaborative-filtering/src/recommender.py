"""Collaborative Filtering Recommendations (Simple Implementation)"""
import numpy as np
import pandas as pd

# Sample ratings data
ratings_data = {
    'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5],
    'item_id': [101, 102, 103, 101, 102, 104, 102, 103, 104, 101, 103, 104, 102, 104],
    'rating': [5, 3, 4, 4, 5, 3, 5, 4, 5, 3, 4, 5, 4, 3]
}

df = pd.DataFrame(ratings_data)

print("📊 COLLABORATIVE FILTERING RECOMMENDATION SYSTEM\n")
print("Sample Ratings:")
print(df.to_string(index=False))

# Create user-item matrix
user_item_matrix = df.pivot(index='user_id', columns='item_id', values='rating').fillna(0)

print("\n\n📋 User-Item Matrix:")
print(user_item_matrix)

# Simple item-based collaborative filtering
# Calculate item similarities (cosine similarity)
def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

# Calculate similarities between items
items = user_item_matrix.columns
item_similarities = {}

for item1 in items:
    item_similarities[item1] = {}
    for item2 in items:
        if item1 != item2:
            similarity = cosine_similarity(
                user_item_matrix[item1].values,
                user_item_matrix[item2].values
            )
            item_similarities[item1][item2] = similarity

print("\n\n🔗 Item Similarities:")
for item, sims in item_similarities.items():
    print(f"\nItem {item}:")
    for similar_item, score in sorted(sims.items(), key=lambda x: x[1], reverse=True)[:2]:
        print(f"  - Item {similar_item}: {score:.3f}")

# Make recommendation for a user
def recommend_for_user(user_id, n_recommendations=3):
    """Recommend items for a user based on item similarities"""
    user_ratings = user_item_matrix.loc[user_id]
    
    # Get items user hasn't rated
    unrated_items = user_ratings[user_ratings == 0].index
    
    # Calculate predicted ratings for unrated items
    predictions = {}
    for item in unrated_items:
        # Find similar items that user has rated
        similar_items = item_similarities.get(item, {})
        
        weighted_sum = 0
        similarity_sum = 0
        
        for similar_item, similarity in similar_items.items():
            if user_ratings[similar_item] > 0:  # User has rated this item
                weighted_sum += similarity * user_ratings[similar_item]
                similarity_sum += abs(similarity)
        
        if similarity_sum > 0:
            predictions[item] = weighted_sum / similarity_sum
    
    # Get top N recommendations
    top_recommendations = sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    return top_recommendations

# Test recommendations
print("\n\n🎯 RECOMMENDATIONS:\n")
for user_id in [1, 3]:
    recommendations = recommend_for_user(user_id, n_recommendations=2)
    print(f"User {user_id}:")
    print(f"  Current ratings: {user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].to_dict()}")
    print(f"  Recommended items:")
    
    if recommendations:
        for item, predicted_rating in recommendations:
            print(f"    - Item {item}: predicted rating {predicted_rating:.2f}")
    else:
        print(f"    - No recommendations available")
    print()

print("✅ Recommendation system completed!")
print("\nThis is a simple item-based collaborative filtering implementation.")
print("For production, consider using libraries like scikit-learn or specialized recommendation engines.")
