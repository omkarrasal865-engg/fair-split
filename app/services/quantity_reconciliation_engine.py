from typing import List

from app.models.reconciliation import UnallocatedQuantity


class QuantityReconciliationEngine:

    def reconcile(
        self,
        receipt,
        allocation_result,
    ) -> List[UnallocatedQuantity]:

        unallocated_items = []

        for item in receipt.items:

            receipt_quantity = item.quantity or 1

            allocated_quantity = 0.0

            for participant in allocation_result:

                for allocated_item in participant.items:

                    allocated_name = allocated_item.split(" (")[0]

                    if allocated_name.lower() != item.name.lower():
                        continue

                    quantity = 1.0

                    if "(" in allocated_item and ")" in allocated_item:
                        try:
                            quantity = float(
                                allocated_item.split("(")[1]
                                .replace(")", "")
                            )
                        except Exception:
                            quantity = 1.0

                    allocated_quantity += quantity

            remaining_quantity = (
                receipt_quantity - allocated_quantity
            )

            if remaining_quantity <= 0:
                continue

            unit_price = item.amount / receipt_quantity

            remaining_amount = (
                remaining_quantity * unit_price
            )

            unallocated_items.append(
                UnallocatedQuantity(
                    item=item.name,
                    total_quantity=receipt_quantity,
                    allocated_quantity=allocated_quantity,
                    remaining_quantity=remaining_quantity,
                    remaining_amount=remaining_amount,
                )
            )

        return unallocated_items