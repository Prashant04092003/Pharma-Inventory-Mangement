from app.schemas.intent_schema import IntentRequest
from app.utils import exceptions


class IntentValidator:

    @staticmethod
    def validate(intent: IntentRequest) -> IntentRequest:

        if intent.intent == "get_store_inventory":
            if intent.store_id is None:
                raise ValueError(exceptions.INVALID_PARAMETERS)

        elif intent.intent == "get_brand_stock_in_store":
            if intent.store_id is None:
                raise ValueError(exceptions.INVALID_PARAMETERS)
            if not intent.brand_name:
                raise ValueError(exceptions.INVALID_PARAMETERS)

        elif intent.intent == "get_global_brand_stock":
            if not intent.brand_name:
                raise ValueError(exceptions.INVALID_PARAMETERS)

        elif intent.intent == "get_low_stock":
            if intent.store_id is None:
                raise ValueError(exceptions.INVALID_PARAMETERS)
            if intent.threshold is None:
                intent.threshold = 50

        else:
            raise ValueError(exceptions.INVALID_INTENT)

        return intent