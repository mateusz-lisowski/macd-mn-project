import pandas as pd
import matplotlib.pyplot as plt


class MacdIndex:

    def __init__(self, data: pd.DataFrame) -> None:

        if 'date' not in data.columns:
            raise ValueError("There is no 'date' column in the input data frame")

        if 'value' not in data.columns:
            raise ValueError("There is no 'value' column in the input data frame")

        self.data = data.copy(deep=True)
        self.data.set_index('date', inplace=True)
        MacdIndex.calculate_macd_index(self.data)

        self.buying_points = MacdIndex.calculate_buying_points(self.data)
        self.selling_points = MacdIndex.calculate_selling_points(self.data)

    @staticmethod
    def calculate_macd_index(df: pd.DataFrame) -> None:
        df['ema12'] = df['value'].ewm(span=12).mean()
        df['ema26'] = df['value'].ewm(span=26).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['signal'] = df['macd'].ewm(span=9).mean()

    @staticmethod
    def calculate_buying_points(df: pd.DataFrame) -> list[int]:
        buying_points: list[int] = []
        for i in range(len(df)):
            if df['macd'].iloc[i] > df['signal'].iloc[i] and df['macd'].iloc[i - 1] < df['signal'].iloc[i - 1]:
                buying_points.append(i)
        return buying_points

    @staticmethod
    def calculate_selling_points(df: pd.DataFrame) -> list[int]:
        selling_points: list[int] = []
        for i in range(len(df)):
            if df['macd'].iloc[i] < df['signal'].iloc[i] and df['macd'].iloc[i - 1] > df['signal'].iloc[i - 1]:
                selling_points.append(i)
        return selling_points

    def plot_macd(self) -> None:
        plt.plot(self.data['signal'], label='signal', color='red')
        plt.plot(self.data['macd'], label='macd', color='green')
        plt.plot(self.data['value'], label='price', color='black')
        plt.scatter(
            self.data.iloc[self.buying_points].index,
            self.data.iloc[self.buying_points]['value'],
            marker='^',
            color='green'
        )
        plt.scatter(
            self.data.iloc[self.selling_points].index,
            self.data.iloc[self.selling_points]['value'],
            marker='v',
            color='red'
        )
        plt.xticks(self.data.index[::60], rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()


def main():
    data = pd.read_csv('data.csv')
    macd = MacdIndex(data)
    macd.plot_macd()


if __name__ == '__main__':
    main()
