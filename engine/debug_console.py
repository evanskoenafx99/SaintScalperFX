class DebugConsole:

    @staticmethod
    def show(results, signal, confidence, buy_score, sell_score):

        print("\n" + "=" * 60)
        print("        SaintScalperFX AI Debug Console")
        print("=" * 60)

        print(f"Signal      : {signal}")
        print(f"Confidence  : {confidence}%")
        print(f"Buy Score   : {buy_score}")
        print(f"Sell Score  : {sell_score}")

        print("\nEngine Results")
        print("-" * 60)

        for result in results:

            print(f"Engine      : {result.get('engine', 'Unknown')}")
            print(f"Signal      : {result.get('signal', 'WAIT')}")
            print(f"Score       : {result.get('score', 0)}")
            print(f"Confidence  : {result.get('confidence', 0)}")
            print(f"Reason      : {result.get('reason', 'No reason')}")
            print("-" * 60)

        print("=" * 60 + "\n")
