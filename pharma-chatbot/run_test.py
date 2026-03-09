from app.llm.intent_extractor import IntentExtractor

extractor = IntentExtractor()
result = extractor.extract("Show low stock in store 3")
print(result)

from app.llm.intent_extractor import IntentExtractor
from app.router.validator import IntentValidator
from app.router.intent_router import IntentRouter

extractor = IntentExtractor()
validator = IntentValidator()
router = IntentRouter()

user_input = "Show low stock in store 3"

intent = extractor.extract(user_input)
validated = validator.validate(intent)
result = router.route(validated)

print(result)