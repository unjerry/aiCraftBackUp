import numpy as np


class Transaction:
    def __init__(self, amount) -> None:
        self.amount = amount

    def __str__(self) -> str:
        return f"<amount={self.amount}>"


class UniLedger:
    def __init__(self, filename: str) -> None:
        self.file = filename
        self.data = self.load()

    def save(self) -> None:
        np.save(self.file, self.data)

    def load(self) -> dict:
        return np.load(self.file, allow_pickle=True).item()

    def add(self, amount: int, date: str) -> None:
        self.data[date] = Transaction(amount)
        self.save()

    def export_list(self):
        for k, v in self.data.items():
            print(k, v)


UniData = UniLedger("sss.npy")
UniData.add(103, "2024-05-25")
UniData.export_list()
