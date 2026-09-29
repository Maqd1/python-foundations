class CollaborativeRecommendation:
    def recommend(self, catalog, members, member, limit=5):
        target_history = set(member.borrowed_resources)

        if not target_history:
            return []

        similarities = []

        for other in members:
            if other is member:
                continue

            other_history = set(other.borrowed_resources)
            shared = target_history & other_history

            if shared:
                similarities.append((len(shared), other))

        similarities.sort(key=lambda item: item[0], reverse=True)

        recommendations = []
        seen = set(target_history)

        for _, other in similarities:
            for resource in other.borrowed_resources:
                if resource in seen:
                    continue

                recommendations.append(resource)
                seen.add(resource)

                if len(recommendations) >= limit:
                    return recommendations

        return recommendations
