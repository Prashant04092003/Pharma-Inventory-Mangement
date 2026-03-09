from app.schemas.intent_schema import IntentRequest
from app.services.inventory_service import InventoryService
from app.utils.exceptions import InvalidIntentException



class IntentRouter:

    def __init__(self):
        self.inventory = InventoryService()

    def route(self, intent: IntentRequest):

        if intent.intent == "get_store_inventory":
            return self.inventory.get_store_inventory(intent.store_id)

        if intent.intent == "get_brand_stock_in_store":
            return self.inventory.get_brand_stock_in_store(
                intent.store_id,
                intent.brand_name
            )

        if intent.intent == "get_global_brand_stock":
            return self.inventory.get_global_brand_stock(
                intent.brand_name
            )

        if intent.intent == "get_low_stock":
            return self.inventory.get_low_stock(
                intent.store_id,
                intent.threshold
            )

        print("ROUTER THROWING INVALIDINTENT")
        raise InvalidIntentException("invalid_intent")