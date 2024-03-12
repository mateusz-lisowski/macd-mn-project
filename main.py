import pandas as pd
import matplotlib.pyplot as plt


def calculate_macd_index(df: pd.DataFrame) -> None:
    df['ema12'] = df['value'].ewm(span=12).mean()
    df['ema26'] = df['value'].ewm(span=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9).mean()


def plot_macd_and_signal(df: pd.DataFrame) -> None:
    plt.plot(df['signal'], label='signal', color='red')
    plt.plot(df['macd'], label='macd', color='green')
    plt.legend()
    plt.show()


def calculate_buying_points(df: pd.DataFrame) -> list:
    buying_points = []
    for i in range(len(df)):
        if df['macd'].iloc[i] > df['signal'].iloc[i] and df['macd'].iloc[i - 1] < df['signal'].iloc[i - 1]:
            buying_points.append(i)
    return buying_points


def calculate_selling_points(df: pd.DataFrame) -> list:
    selling_points = []
    for i in range(len(df)):
        if df['macd'].iloc[i] < df['signal'].iloc[i] and df['macd'].iloc[i - 1] > df['signal'].iloc[i - 1]:
            selling_points.append(i)
    return selling_points


def main():
    data = pd.read_csv('data.csv')
    calculate_macd_index(data)
    plot_macd_and_signal(data)


if __name__ == '__main__':
    main()
