import requests
from app.core.settings import settings


class InventoryService:

    def __init__(self):
        self.base_url = settings.INVENTORY_API_BASE_URL
        self.timeout = settings.INVENTORY_TIMEOUT

    def get_store_inventory(self, store_id: int):
        url = f"{self.base_url}/store/{store_id}/inventory"
        return self._get(url)

    def get_brand_stock_in_store(self, store_id: int, brand_name: str):
        url = f"{self.base_url}/store/{store_id}/brand/{brand_name}"
        return self._get(url)

    def get_global_brand_stock(self, brand_name: str):
        url = f"{self.base_url}/brand/{brand_name}/global-stock"
        return self._get(url)

    def get_low_stock(self, store_id: int, threshold: int):
        url = f"{self.base_url}/store/{store_id}/low-stock"
        params = {"threshold": threshold}
        return self._get(url, params=params)

    def _get(self, url: str, params: dict | None = None):
        response = requests.get(url, params=params, timeout=self.timeout)

        if response.status_code == 404:
            return {"error": "Not found"}

        response.raise_for_status()
        return response.json()
   