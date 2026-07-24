import { View, Text, StyleSheet, ScrollView } from "react-native";

function MetricCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <View style={styles.metricCard}>
      <Text style={styles.metricTitle}>{title}</Text>
      <Text style={styles.metricValue}>{value}</Text>
    </View>
  );
}

export default function HomeScreen() {
  return (
    <ScrollView style={styles.container}>

      <Text style={styles.title}>SaintScalperFX</Text>
      <Text style={styles.subtitle}>AI Trading Engine</Text>

      <View style={styles.aiCard}>

        <Text style={styles.aiAvatar}>🤖</Text>

        <Text style={styles.online}>🟢 AI ONLINE</Text>

        <Text style={styles.signalLabel}>CURRENT SIGNAL</Text>

        <Text style={styles.buy}>BUY</Text>

        <Text style={styles.details}>
          Symbol: XAUUSD{"\n"}
          Timeframe: M5{"\n"}
          Confidence: 94%
        </Text>

      </View>
      <Text style={styles.section}>Trading Analytics</Text>

      <View style={styles.grid}>
        <MetricCard title="Balance" value="R180,000" />
        <MetricCard title="Equity" value="R182,450" />
        <MetricCard title="Today's Profit" value="+R3,250" />
        <MetricCard title="Win Rate" value="78%" />
        <MetricCard title="Drawdown" value="1.4%" />
        <MetricCard title="Profit Factor" value="2.8" />
      </View>

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
  },

  subtitle: {
    color: "#8A94A6",
    fontSize: 18,
    marginBottom: 20,
  },

  aiCard: {
    backgroundColor: "#0B1228",
    borderRadius: 24,
    padding: 25,
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#00AEEF",
    marginBottom: 25,
  },

  aiAvatar: {
    fontSize: 80,
  },

  online: {
    color: "#00FF99",
    fontSize: 18,
    fontWeight: "bold",
    marginTop: 10,
  },

  signalLabel: {
    color: "#9CA3AF",
    marginTop: 20,
  },

  buy: {
    color: "#00FF99",
    fontSize: 42,
    fontWeight: "bold",
    marginTop: 8,
  },

  details: {
    color: "#FFFFFF",
    textAlign: "center",
    fontSize: 16,
    lineHeight: 28,
    marginTop: 15,
  },
  section: {
    color: "#FFFFFF",
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 15,
  },

  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
  },

  metricCard: {
    width: "48%",
    backgroundColor: "#101827",
    borderRadius: 18,
    padding: 18,
    marginBottom: 15,
  },

  metricTitle: {
    color: "#9CA3AF",
    fontSize: 14,
  },

  metricValue: {
    color: "#00AEEF",
    fontSize: 22,
    fontWeight: "bold",
    marginTop: 8,
  },

});
