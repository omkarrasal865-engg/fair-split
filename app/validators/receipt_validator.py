from app.models.raw_receipt import RawReceiptExtraction
from app.models.receipt import Receipt, ReceiptItem
from app.models.validation import ReceiptValidationResult

from app.services.expense_classifier import (
    ExpenseClassifier,
)


class ReceiptValidator:

    def __init__(self):
        self.expense_classifier = (
            ExpenseClassifier()
        )

    def validate(
        self,
        raw_receipt: RawReceiptExtraction
    ) -> ReceiptValidationResult:

        assumptions = []
        flags = []

        subtotal = raw_receipt.subtotal

        if subtotal is None:
            subtotal = sum(
                item.amount
                for item in raw_receipt.items
            )

            assumptions.append(
                "Subtotal missing; calculated from line items."
            )

        service_charge = (
            raw_receipt.service_charge
        )

        if service_charge is None:
            service_charge = 0

            assumptions.append(
                "Service charge not present on receipt; treated as ₹0."
            )

        tax = raw_receipt.tax

        if tax is None:
            tax = 0

            assumptions.append(
                "Tax not present on receipt; treated as ₹0."
            )

        discount = raw_receipt.discount

        if discount is None:
            discount = 0

            assumptions.append(
                "Discount not present on receipt; treated as ₹0."
            )

        grand_total = (
            raw_receipt.grand_total
        )

        if grand_total is None:

            grand_total = (
                subtotal
                + service_charge
                + tax
                - discount
            )

            assumptions.append(
                "Grand total missing; calculated from available values."
            )

        item_total = sum(
            item.amount
            for item in raw_receipt.items
        )

        if abs(item_total - subtotal) > 1:
            flags.append(
                f"Line items total ₹{item_total:.2f} "
                f"does not match subtotal ₹{subtotal:.2f}."
            )

        expected_grand_total = (
            subtotal
            + service_charge
            + tax
            - discount
        )

        if (
            abs(
                expected_grand_total
                - grand_total
            )
            > 1
        ):
            flags.append(
                f"Expected grand total ₹{expected_grand_total:.2f} "
                f"does not match extracted grand total ₹{grand_total:.2f}."
            )

        receipt_items = [
            ReceiptItem(
                name=item.name,
                quantity=item.quantity or 1,
                amount=item.amount,
            )
            for item in raw_receipt.items
        ]

        expense_category = (
            self.expense_classifier.classify(
                merchant_name=raw_receipt.restaurant_name,
                raw_text=raw_receipt.raw_text,
            )
        )

        receipt = Receipt(
            items=receipt_items,
            subtotal=subtotal,
            service_charge=service_charge,
            tax=tax,
            discount=discount,
            grand_total=grand_total,
            merchant_name=raw_receipt.restaurant_name,
            expense_category=expense_category,
        )

        return ReceiptValidationResult(
            receipt=receipt,
            assumptions=assumptions,
            flags=flags,
        )