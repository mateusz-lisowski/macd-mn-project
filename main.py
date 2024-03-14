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

    def plot_macd(self, title: str) -> None:

        plt.plot(self.data['signal'], label='signal', color='red')
        plt.plot(self.data['macd'], label='macd', color='green')

        plt.xticks(self.data.index[::60], rotation=45)
        plt.tight_layout()

        plt.xlabel('date')
        plt.ylabel('macd/signal value')
        plt.title(title)

        plt.legend()
        plt.show()

    def plot_assets_with_buy_sell_points(self, title: str):

        plt.plot(self.data['value'], label='price', color='black')

        plt.scatter(
            self.data.iloc[self.buying_points].index,
            self.data.iloc[self.buying_points]['value'],
            label='buying points',
            marker='^',
            color='green'
        )

        plt.scatter(
            self.data.iloc[self.selling_points].index,
            self.data.iloc[self.selling_points]['value'],
            label='selling points',
            marker='v',
            color='red'
        )

        plt.xticks(self.data.index[::60], rotation=45)
        plt.tight_layout()

        plt.xlabel('date')
        plt.ylabel('asset price [PLN]')
        plt.title(title)

        plt.legend()
        plt.show()

    def backtest(self, start_assets: float = None) -> tuple[float, float]:

        buy_days = [day + 1 for day in self.buying_points]
        sell_days = [day + 1 for day in self.selling_points]

        buy_prices: pd.DataFrame = self.data['value'].iloc[buy_days]
        sell_prices: pd.DataFrame = self.data['value'].iloc[sell_days]

        if sell_prices.index[0] < buy_prices.index[0]:
            sell_prices.drop(sell_prices.index[0], inplace=True)

        if buy_prices.index[-1] > sell_prices.index[-1]:
            buy_prices.drop(buy_prices.index[-1], inplace=True)

        profits: list[float] = []
        for buy_price, sell_price in zip(buy_prices, sell_prices):
            profit = (sell_price - buy_price) / buy_price
            profits.append(profit)

        total = start_assets
        if start_assets:
            for buy_price, sell_price in zip(buy_prices, sell_prices):
                assets = total / buy_price
                revenue = assets * sell_price
                total = revenue

        return sum(profits) / len(profits), total


def get_df_from_csv_file(filepath: str) -> pd.DataFrame | None:
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return None


def main():

    usd = get_df_from_csv_file('data/usd.csv')
    if usd is None:
        print("There is no valid csv file under given path")

    eur = get_df_from_csv_file('data/eur.csv')
    if eur is None:
        print("There is no valid csv file under given path")

    chf = get_df_from_csv_file('data/chf.csv')
    if chf is None:
        print("There is no valid csv file under given path")

    usd_macd = MacdIndex(usd)
    eur_macd = MacdIndex(eur)
    chf_macd = MacdIndex(chf)

    usd_macd.plot_macd('MACD and SIGNAL value for USD')
    usd_macd.plot_assets_with_buy_sell_points('USD price in PLN with buying and selling points')

    eur_macd.plot_macd('MACD and SIGNAL value for EUR')
    eur_macd.plot_assets_with_buy_sell_points('EUR price in PLN with buying and selling points')

    chf_macd.plot_macd('MACD and SIGNAL value for CHF')
    chf_macd.plot_assets_with_buy_sell_points('CHF price in PLN with buying and selling points')

    START_CAPITAL = 1000

    usd_result = usd_macd.backtest(START_CAPITAL)
    print(f"Average profit for 1000 trading days for USD is: {usd_result[0]:.8f}")
    print(f"If you started with {START_CAPITAL} USD on the begging, you would have {usd_result[1]:.2f} USD at the end")

    eur_result = eur_macd.backtest(START_CAPITAL)
    print(f"Average profit for 1000 trading days for EUR is: {eur_result[0]:.8f}")
    print(f"If you started with {START_CAPITAL} EUR on the begging, you would have {eur_result[1]:.2f} EUR at the end")

    chf_result = chf_macd.backtest(START_CAPITAL)
    print(f"Average profit for 1000 trading days for CHF is: {chf_result[0]:.8f}")
    print(f"If you started with {START_CAPITAL} CHF on the begging, you would have {chf_result[1]:.2f} CHF at the end")


if __name__ == '__main__':
    main()
