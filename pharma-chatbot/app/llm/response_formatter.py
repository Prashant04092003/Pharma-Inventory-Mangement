from typing import List, Dict


class ResponseFormatter:

    @staticmethod
    def format_low_stock(items, threshold=50):

        if not items:
            return {
                "summary": "No low stock medicines found.",
                "critical_count": 0,
                "warning_count": 0,
                "total_items": 0,
                "top_critical": []
            }

        # Sort by stock ascending
        sorted_items = sorted(items, key=lambda x: x["current_stock"])

        # Categorize
        critical = [i for i in sorted_items if i["current_stock"] == 0]
        warning = [i for i in sorted_items if 0 < i["current_stock"] <= 10]
        low = [i for i in sorted_items if 10 < i["current_stock"] <= threshold]

        # Top 10 most urgent items
        top_critical = [
            f'{i["brand_name"]} ({i["current_stock"]} units)'
            for i in sorted_items[:10]
        ]

        if len(critical) > 100:
            health_status = "CRITICAL"
        elif len(critical) > 20:
            health_status = "WARNING"
        else:
            health_status = "STABLE"

        return {
            "summary": f"{len(items)} medicines are below stock threshold.",
            "stock_health": health_status,
            "critical_count": len(critical),
            "warning_count": len(warning),
            "low_count": len(low),
            "total_items": len(items),
            "reorder_recommended": len(critical) > 0,
            "top_urgent_items": top_critical
            }
    @staticmethod
    def format_inventory(items):

        if not items:
            return {
                "summary": "No inventory found for this store.",
                "total_items": 0,
                "items": []
            }

        return {
            "summary": f"{len(items)} medicines found in inventory.",
            "total_items": len(items),
            "items": items[:50]  # limit to first 50 to avoid huge payload
        }