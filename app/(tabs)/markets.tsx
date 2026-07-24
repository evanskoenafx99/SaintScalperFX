import { View, Text, StyleSheet, ScrollView } from "react-native";

function MarketCard({
  symbol,
  signal,
  confidence,
  color,
}: {
  symbol: string;
  signal: string;
  confidence: string;
  color: string;
}) {
  return (
    <View style={styles.card}>
      <Text style={styles.symbol}>{symbol}</Text>

      <Text style={[styles.signal, { color }]}>
        {signal}
      </Text>

      <Text style={styles.confidence}>
        Confidence: {confidence}
      </Text>
    </View>
  );
}

export default function MarketsScreen() {
  return (
    <ScrollView style={styles.container}>

      <Text style={styles.title}>Markets</Text>

      <MarketCard
        symbol="XAUUSD"
        signal="BUY"
        confidence="94%"
        color="#00FF99"
      />

      <MarketCard
        symbol="EURUSD"
        signal="SELL"
        confidence="88%"
        color="#FF4C4C"
      />

      <MarketCard
        symbol="GBPUSD"
        signal="BUY"
        confidence="81%"
        color="#00FF99"
      />

      <MarketCard
        symbol="BTCUSD"
        signal="WAIT"
        confidence="72%"
        color="#FFD54A"
      />

      <MarketCard
        symbol="US30"
        signal="BUY"
        confidence="90%"
        color="#00FF99"
      />

      <MarketCard
        symbol="NAS100"
        signal="BUY"
        confidence="86%"
        color="#00FF99"
      />

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050816",
    padding: 20,
  },

  title: {
    color: "#00AEEF",
    fontSize: 32,
    fontWeight: "bold",
    marginTop: 40,
    marginBottom: 25,
  },

  card: {
    backgroundColor: "#101827",
    borderRadius: 18,
    padding: 20,
    marginBottom: 15,
  },

  symbol: {
    color: "#FFFFFF",
    fontSize: 22,
    fontWeight: "bold",
  },

  signal: {
    fontSize: 20,
    fontWeight: "bold",
    marginTop: 8,
  },

  confidence: {
    color: "#9CA3AF",
    marginTop: 8,
    fontSize: 16,
  },
});
