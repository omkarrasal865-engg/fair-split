class FairSplitException(
    Exception
):
    pass


class ReceiptExtractionError(
    FairSplitException
):
    pass


class RulesExtractionError(
    FairSplitException
):
    pass


class GeminiServiceError(
    FairSplitException
):
    pass


class AllocationError(
    FairSplitException
):
    pass


class ValidationError(
    FairSplitException
):
    pass