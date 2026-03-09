import json
from pydantic import ValidationError

from app.llm.llm_client import LLMClient
from app.schemas.intent_schema import IntentRequest
from app.constants import SUPPORTED_INTENTS
from app.utils.exceptions import InvalidIntentException
from app.utils.exceptions import INVALID_INTENT


SYSTEM_PROMPT = """
You are a strict intent extraction engine for a pharmaceutical inventory system.

Return ONLY valid JSON.
Do NOT explain.
Do NOT generate SQL.
Do NOT include any text outside JSON.

Allowed intents:
- get_store_inventory
- get_brand_stock_in_store
- get_global_brand_stock
- get_low_stock

Schema:
{
  "intent": string,
  "store_id": integer | null,
  "brand_name": string | null,
  "threshold": integer | null
}

Rules:

1. If user asks for entire store inventory, use:
   intent = get_store_inventory

2. If user mentions a specific brand name AND refers to a store,
   intent MUST be get_brand_stock_in_store.

   Examples:
   - "How much Alex Syrup is in my store?"
   - "Stock of Paracetamol in store 2"
   - "Do we have Allegra in store 1?"

   These MUST NOT be classified as get_store_inventory.

3. If user asks for stock of a brand across all stores,
   intent = get_global_brand_stock.

4. If user asks for low stock items in a store,
   intent = get_low_stock.

5. If unclear, return:
   {
     "intent": "unknown"
   }

"""


class IntentExtractor:
    def __init__(self):
        self.client = LLMClient()

    def extract(self, user_input: str) -> IntentRequest:
        raw_output = self.client.generate(
            prompt=user_input,
            system=SYSTEM_PROMPT
        )

        #  Try parsing JSON
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            raise InvalidIntentException(INVALID_INTENT)

        #  Validate intent existence
        intent = parsed.get("intent")
        if intent not in SUPPORTED_INTENTS:
            raise InvalidIntentException(INVALID_INTENT)

        #  Validate schema using Pydantic
        try:
            validated_intent = IntentRequest(**parsed)
        except ValidationError:
            raise InvalidIntentException(INVALID_INTENT)

        return validated_intent