from collections import Counter


class RecommendationService:

    def recommend_by_genre(
        self,
        catalog,
        genre,
        limit=5,
    ):
        results = [
            resource
            for resource in catalog.resources
            if resource.genre.lower() == genre.lower()
        ]

        return results[:limit]

    def recommend_by_author(
        self,
        catalog,
        author,
        limit=5,
    ):
        author = author.lower()

        results = [
            resource
            for resource in catalog.resources
            if any(
                author in item.lower()
                for item in resource.authors
            )
        ]

        return results[:limit]

    def recommend_by_history(
        self,
        catalog,
        borrowed_resources,
        limit=5,
    ):
        if not borrowed_resources:
            return []

        genres = Counter(
            resource.genre
            for resource in borrowed_resources
        )

        recommendations = []

        for genre, _ in genres.most_common():
            for resource in catalog.resources:
                if resource in borrowed_resources:
                    continue

                if resource.genre == genre:
                    recommendations.append(resource)

                if len(recommendations) >= limit:
                    return recommendations

        return recommendations

    def popular_resources(
        self,
        resources,
        limit=5,
    ):
        return sorted(
            resources,
            key=lambda resource: resource.borrowed_copies,
            reverse=True,
        )[:limit]