import warnings
warnings.filterwarnings('ignore')

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import polars as pl
from poly_utils.utils import get_markets, update_missing_tokens

import subprocess


def get_processed_df(df):
    markets_df = get_markets()
    markets_df = markets_df.rename({'id': 'market_id'})

    # 1) Make markets long: (market_id, side, asset_id) where side ∈ {"token1", "token2"}
    markets_long = (
        markets_df
        .select(["market_id", "token1", "token2"])
        .melt(id_vars="market_id", value_vars=["token1", "token2"],
            variable_name="side", value_name="asset_id")
    )

    # 2) Identify the non-USDC asset for each trade (the one that isn't 0)
    df = df.with_columns(
        pl.when(pl.col("makerAssetId") != "0")
        .then(pl.col("makerAssetId"))
        .otherwise(pl.col("takerAssetId"))
        .alias("nonusdc_asset_id")
    )

    # 3) Join once on that non-USDC asset to recover the market + side ("token1" or "token2")
    df = df.join(
        markets_long,
        left_on="nonusdc_asset_id",
        right_on="asset_id",
        how="left",
    )

    # 4) label columns and keep market_id
    df = df.with_columns([
        pl.when(pl.col("makerAssetId") == "0").then(pl.lit("USDC")).otherwise(pl.col("side")).alias("makerAsset"),
        pl.when(pl.col("takerAssetId") == "0").then(pl.lit("USDC")).otherwise(pl.col("side")).alias("takerAsset"),
        pl.col("market_id"),
    ])

    df = df[['timestamp', 'market_id', 'maker', 'makerAsset', 'makerAmountFilled', 'taker', 'takerAsset', 'takerAmountFilled', 'transactionHash']]

    df = df.with_columns([
        (pl.col("makerAmountFilled") / 10**6).alias("makerAmountFilled"),
        (pl.col("takerAmountFilled") / 10**6).alias("takerAmountFilled"),
    ])

    df = df.with_columns(
        pl.when(pl.col("takerAsset") == "USDC")
        .then(pl.lit("BUY"))
        .otherwise(pl.lit("SELL"))
        .alias("taker_direction")
    )

    df = df.with_columns([
        pl.when(pl.col("takerAsset") == "USDC")
        .then(pl.lit("BUY"))
        .otherwise(pl.lit("SELL"))
        .alias("taker_direction"),

        # reverse of taker_direction
        pl.when(pl.col("takerAsset") == "USDC")
        .then(pl.lit("SELL")),
        .otherwise(pl.lit("BUY")),
        .alias("maker_direction"),
    ])

    df = df.with_columns([
        pl.when(pl.col("makerAsset") != "USDC")
        .then(pl.col("makerAsset"))
        .otherwise(pl.col("takerAsset"))
        .alias("nonusdc_side"),

        pl.when(pl.col("takerAsset") == "USDC")
        .then(pl.col("takerAmountFilled"))
        .otherwise(pl.col("makerAmountFilled"))
        .alias("usd_amount"),
        pl.when(pl.col("takerAsset") != "USDC")
        .then(pl.col("takerAmountFilled"))
        .otherwise(pl.col("makerAmountFilled")),
        .alias("token_amount"),
        pl.when(pl.col("takerAsset") == "USDC")
        .then(pl.col("takerAmountFilled") / pl.col("makerAmountFilled")),
        .otherwise(pl.col("makerAmountFilled") / pl.col("takerAmountFilled")),
        .cast(pl.Float64)
        .alias("price")
    ])


    df = df[['timestamp', 'market_id', 'maker', 'taker', 'nonusdc_side', 'maker_direction', 'taker_direction', 'price', 'usd_amount', 'token_amount', 'transactionHash']]
    return df


def process_live():
    processed_file = 'processed/trades.csv'

    print("=" * 60)
    print("🔄 Processing Live Trades")
    print("=" * 60)

    last_processed_timestamp = 0

    if os.path.exists(processed_file):
        print(f"✓ Found existing processed file: {processed_file}")
        try:
            last_processed_timestamp = pl.read_csv(processed_file).select(pl.max('timestamp')).item()
            if last_processed_timestamp:
                print(f"📍 Resuming from: {last_processed_timestamp}")
        except Exception as e:
            print(f"Could not read last processed timestamp: {e}")

    else:
        print("⚠ No existing processed file found - processing from beginning")

    print(f"\n📂 Reading: goldsky/orderFilled")

    schema_overrides = {
        "takerAssetId": pl.Utf8,
        "makerAssetId": pl.Utf8,
    }

    df = pl.scan_parquet("goldsky/orderFilled/**/*.parquet", schema_overrides=schema_overrides).collect(streaming=True)
    df = df.with_columns(
        pl.from_epoch(pl.col('timestamp'), time_unit='s').alias('timestamp')
    )

    print(f"✓ Loaded {len(df):,} rows")

    if last_processed_timestamp:
        df_process = df.filter(pl.col('timestamp') > last_processed_timestamp)
    else:
        df_process = df

    print(f"⚙️  Processing {len(df_process):,} new rows...")

    if len(df_process) > 0:
        new_df = get_processed_df(df_process)

        if not os.path.isdir('processed'):
            os.makedirs('processed')

        op_file = 'processed/trades.csv'

        if not os.path.isfile(op_file):
            new_df.write_csv(op_file)
            print(f"✓ Created new file: processed/trades.csv")
        else:
            print(f"✓ Appending {len(new_df):,} rows to processed/trades.csv")
            with open(op_file, mode="a") as f:
                new_df.write_csv(f, include_header=False)

    print("=" * 60)
    print("✅ Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    process_live()
