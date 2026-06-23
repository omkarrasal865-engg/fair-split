class ExpenseClassifier:

    def classify(
        self,
        merchant_name: str | None,
        raw_text: str,
    ) -> str:

        text = (
            f"{merchant_name or ''} {raw_text}"
        ).lower()

        restaurant_keywords = [
            "restaurant",
            "cafe",
            "biriyani",
            "pizza",
            "food",
            "bar",
        ]

        grocery_keywords = [
            "dmart",
            "supermarket",
            "grocery",
            "mart",
            "fresh",
        ]

        travel_keywords = [
            "uber",
            "ola",
            "flight",
            "airways",
            "railway",
            "fuel",
            "petrol",
        ]

        if any(
            keyword in text
            for keyword in restaurant_keywords
        ):
            return "Restaurant"

        if any(
            keyword in text
            for keyword in grocery_keywords
        ):
            return "Grocery"

        if any(
            keyword in text
            for keyword in travel_keywords
        ):
            return "Travel"

        return "Other"