class DebugConsole:

    @staticmethod
    def show(results, signal, confidence, buy_score, sell_score):
        print("\n==============================")
        print("   SAINTSCALPERFX AI")
        print("==============================")

        for engine, value in results.items():
            print(f"{engine:<15}: {value}")

        print("------------------------------")
        print(f"BUY Score      : {buy_score}")
        print(f"SELL Score     : {sell_score}")
        print(f"Confidence     : {confidence}%")
        print(f"FINAL SIGNAL   : {signal}")
        print("==============================\n")
