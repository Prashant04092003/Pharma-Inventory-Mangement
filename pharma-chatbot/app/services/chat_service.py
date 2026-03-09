import json
from app.llm.intent_extractor import IntentExtractor
from app.router.intent_router import IntentRouter
from app.llm.response_formatter import ResponseFormatter
from app.llm.llm_client import LLMClient
from app.services.memory_service import MemoryService
from app.utils.exceptions import InvalidIntentException
from app.utils import exceptions


class ChatService:

    def __init__(self):
        self.extractor = IntentExtractor()
        self.router = IntentRouter()
        self.llm = LLMClient()

    def process(self, message: str, role: str , store_id: int | None = None, session_id: str = None):
        try:
            if role is None:
                  raise ValueError("Role must be provided.")
            if session_id is None:
                 raise ValueError("Session ID must be provided.")
            # Step 1: Extract intent
            intent = self.extractor.extract(message)
            if intent.intent not in ["get_store_inventory","get_brand_stock_in_store","get_global_brand_stock","get_low_stock"]:
                raise InvalidIntentException("invalid_intent")

            # --------------------------------------------------
            # Step 2: Role enforcement & default injection
            # --------------------------------------------------
            if role == "SHOP_OPERATOR":
                # Operator logic
                    # Auto-assign their store if not provided
                    if store_id is None:
                        raise ValueError("Store ID must be provided for shop operator.")
                    if intent.store_id is None:
                        intent.store_id = store_id
                    # Block access to other stores
                    elif intent.store_id != store_id:
                        raise ValueError("Access denied: You can only access your assigned store.")
                    

                # Admin logic
            elif role == "ADMIN":
                    # Admin must specify store for store-specific queries
                if intent.intent in ["get_store_inventory", "get_low_stock"]:
                    if intent.store_id is None:
                        raise ValueError("Admin must specify a store_id.")
            elif role is None:
                raise ValueError("Role must be provided.")
            
            # --------------------------------------------------
            # Step 3: Inject threshold default
            # --------------------------------------------------
            if intent.intent == "get_low_stock":
                if intent.threshold is None:
                    intent.threshold = 50
            # --------------------------------------------------
            # Step 4: Route to backend
            # --------------------------------------------------
            result = self.router.route(intent)

            # --------------------------------------------------
            # Step 5: Format output
            # --------------------------------------------------
            if intent.intent == "get_low_stock":
                formatted = ResponseFormatter.format_low_stock(
                    result,
                    threshold=intent.threshold
                )

            elif intent.intent == "get_store_inventory":
                formatted = ResponseFormatter.format_inventory(result)

            else:
                # Fallback — still structured
                formatted = result

            MemoryService.save_message(session_id, "user", message)
            MemoryService.save_message(session_id, "assistant", json.dumps(formatted))

            return {
                "success": True,
                "data": formatted,
                "error": None
            }
        except InvalidIntentException as e:

            # Converstional Fallback
            history = MemoryService.get_history(session_id)
            conversation_prompt = ""
            for item in history:
                conversation_prompt += f"{item['role']}: {item['message']}\n"

            conversation_prompt += f"user: {message}\nassistant:"

            system_prompt = (
                "You are a helpful pharmacy assistant chatbot. "
                "Answer politely and concisely."
            )

            llm_response = self.llm.generate(
                prompt=conversation_prompt,
                system=system_prompt
            )

            MemoryService.save_message(session_id, "user", message)
            MemoryService.save_message(session_id, "assistant", llm_response)

            return {
                "success": True,
                "data": {
                    "response": llm_response
                },
                "error": None,
            }


        except ValueError as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

        except Exception as e:
            print("CHAT SERVICE ERROR:", str(e))
            return {
                "success": False,
                "data": None,
                "error": exceptions.BACKEND_ERROR
            }