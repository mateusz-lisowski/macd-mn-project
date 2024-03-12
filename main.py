import pandas as pd
import matplotlib.pyplot as plt


def calculate_macd_index(df: pd.DataFrame) -> None:
    df['ema12'] = df['value'].ewm(span=12).mean()
    df['ema26'] = df['value'].ewm(span=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9).mean()


def plot_macd(df: pd.DataFrame, buying_points: list[int], selling_points: list[int]) -> None:
    plt.plot(df['signal'], label='signal', color='red')
    plt.plot(df['macd'], label='macd', color='green')
    plt.plot(df['value'], label='price', color='black')
    plt.scatter(df.iloc[buying_points].index, df.iloc[buying_points]['value'], marker='^', color='green')
    plt.scatter(df.iloc[selling_points].index, df.iloc[selling_points]['value'], marker='v', color='red')
    plt.legend()
    plt.show()


def calculate_buying_points(df: pd.DataFrame) -> list[int]:
    buying_points: list[int] = []
    for i in range(len(df)):
        if df['macd'].iloc[i] > df['signal'].iloc[i] and df['macd'].iloc[i - 1] < df['signal'].iloc[i - 1]:
            buying_points.append(i)
    return buying_points


def calculate_selling_points(df: pd.DataFrame) -> list:
    selling_points: list[int] = []
    for i in range(len(df)):
        if df['macd'].iloc[i] < df['signal'].iloc[i] and df['macd'].iloc[i - 1] > df['signal'].iloc[i - 1]:
            selling_points.append(i)
    return selling_points


def main():
    data = pd.read_csv('data.csv')
    calculate_macd_index(data)
    buying_points = calculate_buying_points(data)
    selling_points = calculate_selling_points(data)
    plot_macd(data, buying_points, selling_points)


if __name__ == '__main__':
    main()
