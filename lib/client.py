from .utils.api import Api


class Client(Api):
    def __init__(
        self, debug: bool = True, token: str = None, storeId: str = None
    ) -> None:
        super().__init__(debug)
        self.token = token
        self.storeId = storeId
        self.headers = {"Authorization": f"{self.token}"}

    def login(self, email: str, password: str):
        """
        `Parâmetros`:
            email (str): Email do cliente
            password (str): Senha do cliente

        `Retorna`:
            self.token

        `Exemplo de uso`:
            >>> from lib.client import Client
            >>> client = Client()
            >>> client.login(email="vitor.dev@mail.com", password="12345")
        """
        response = self.sendPost("login", json={"email": email, "password": password})
        token = response.json()["token"]
        if token:
            self.token = token
        return response

    def fetch_store_info(self):
        """
        Retorna as informações da loja que estiver instanciada.
        `Como retornar o JSON`:
            >>> from lib.client import Client
            >>> client = Client()
            >>> if client.login("meu_email@gmail.com", "minhasenha321"):
            >>>     info = client.fetch_store_info().json()
            >>>     print(info)
        """
        response = self.sendGet(
            "user-stores", headers={"Authorization": f"{self.token}"}
        )
        return response

    def fetch_store_id(self, token: str = None) -> str:
        """Retorne apenas o `storeId` com ou sem o parâmetro `token`. É preciso ter feito login para usar."""
        self.headers = {"Authorization": f"{self.token if self.token else token}"}
        response = self.sendGet("user-stores", headers=self.headers)

        s = response.json()
        if s and isinstance(s, list) and len(s) > 0:
            stId = s[0]["id"]
            self.storeId = stId
            return stId

    def set_token(self, token=None):
        """Atribua a `self.token` um novo valor sem fazer login."""
        self.token = token if token else None
        if self.token:
            return True
        else:
            return False

    def set_product(self, products=list, storeId: str = None, **kwargs):
        response = self.sendPost(
            "import/store-product",
            json={
                "storeId": self.storeId if not self.storeId else storeId,
                "products": products,
            },
            headers=self.headers,
        )
        return response

    def fetch_my_products(self, storeId=str, page=int):
        response = self.sendGet(
            endpoint="product",
            params={
                "store_id": storeId if storeId else self.storeId,
                "page": page,
            },
            headers=self.headers,
        )
        return response.json()["items"]

    def delete_all_products(self, storeId: int = None):
        response = self.sendDelete(
            endpoint="product-bulk",
            params={
                "store_id": storeId if storeId else self.storeId,
            },
            headers=self.headers,
        )
        return response.json()
