class ReportingService:

    def inventory_report(self, catalog):
        lines = [
            "LIBRARY INVENTORY REPORT",
            "=" * 40,
        ]

        for resource in catalog.resources:
            lines.append(
                f"{resource.title} | "
                f"ISBN: {resource.isbn} | "
                f"Copies: {resource.copies} | "
                f"Available: {resource.available_copies}"
            )

        return "\n".join(lines)

    def availability_report(self, catalog):
        total = sum(
            resource.copies
            for resource in catalog.resources
        )

        available = sum(
            resource.available_copies
            for resource in catalog.resources
        )

        borrowed = total - available

        return "\n".join([
            "LIBRARY AVAILABILITY REPORT",
            "=" * 40,
            f"Total copies: {total}",
            f"Available copies: {available}",
            f"Borrowed copies: {borrowed}",
        ])

    def resource_summary(self, catalog):
        return {
            "resources": len(catalog.resources),
            "copies": sum(
                resource.copies
                for resource in catalog.resources
            ),
            "available": sum(
                resource.available_copies
                for resource in catalog.resources
            ),
            "borrowed": sum(
                resource.borrowed_copies
                for resource in catalog.resources
            ),
        }