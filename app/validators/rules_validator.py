from app.models.raw_rules import RawRulesExtraction
from app.models.rules import (
    ConsumptionRules,
    OwnershipRule,
    ExclusionRule,
    PaymentRule,
)


class RulesValidator:
    def validate(
        self,
        raw_rules: RawRulesExtraction
    ) -> ConsumptionRules:

        assumptions = []
        flags = []

        participants = list(
            dict.fromkeys(
                raw_rules.participants
            )
        )

        participant_set = set(
            participants
        )

        valid_ownership_rules = []

        for rule in raw_rules.ownership_rules:

            if not rule.consumers:
                flags.append(
                    f"Item '{rule.item}' has no consumers."
                )
                continue

            unknown_consumers = [
                consumer
                for consumer in rule.consumers
                if consumer not in participant_set
            ]

            if unknown_consumers:
                flags.append(
                    f"Item '{rule.item}' references unknown consumers: "
                    f"{', '.join(unknown_consumers)}."
                )

            valid_ownership_rules.append(
                OwnershipRule(
                    item=rule.item,
                    consumers=rule.consumers,
                )
            )

        valid_exclusion_rules = []

        for rule in raw_rules.exclusion_rules:

            if rule.person not in participant_set:
                flags.append(
                    f"Exclusion rule references unknown participant "
                    f"'{rule.person}'."
                )

            valid_exclusion_rules.append(
                ExclusionRule(
                    person=rule.person,
                    item=rule.item,
                )
            )

        valid_payments = []

        for payment in raw_rules.payments:

            if payment.person not in participant_set:
                flags.append(
                    f"Payment references unknown participant "
                    f"'{payment.person}'."
                )

            valid_payments.append(
                PaymentRule(
                    person=payment.person,
                    amount=payment.amount,
                )
            )

        if not valid_payments:
            assumptions.append(
                "No payer explicitly mentioned."
            )

        return ConsumptionRules(
            participants=participants,
            ownership_rules=valid_ownership_rules,
            exclusion_rules=valid_exclusion_rules,
            payments=valid_payments,
            shared_remaining_items=
                raw_rules.shared_remaining_items,
            assumptions=assumptions,
            flags=flags,
        )