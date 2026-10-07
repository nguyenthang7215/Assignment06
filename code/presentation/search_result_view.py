from domain.models import Order, RankedResult


class SearchResultView:
    @staticmethod
    def render_results(title: str, query: str, results: list[RankedResult]) -> None:
        print(f"\n=== {title} ===")
        print(f"Input: {query}")
        print("Processing: normalize/encode -> retrieve -> rank")
        if not results:
            print("No matching product.")
            return
        for position, result in enumerate(results, start=1):
            product = result.product
            print(
                f"{position}. {product.name} | price=${product.price:.2f} "
                f"| score={result.score:.4f} | {result.reason}"
            )

    @staticmethod
    def render_order(order: Order | None) -> None:
        print("\n=== Order Search ===")
        if order is None:
            print("Order not found.")
            return
        print(
            f"Order: {order.order_id} | customer={order.customer_id} "
            f"| date={order.date} | status={order.status} | total=${order.total:.2f}"
        )


