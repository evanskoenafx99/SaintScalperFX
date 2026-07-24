import { View, Text, StyleSheet } from "react-native";

export default function AnalyticsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Analytics</Text>

      <View style={styles.card}>
        <Text style={styles.label}>Today's Profit</Text>
        <Text style={styles.value}>+R3,250</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>Win Rate</Text>
        <Text style={styles.value}>78%</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>Profit Factor</Text>
        <Text style={styles.value}>2.8</Text>
      </View>
    </View>
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
    fontSize: 30,
    fontWeight: "bold",
    marginTop: 40,
    marginBottom: 30,
  },

  card: {
    backgroundColor: "#101827",
    borderRadius: 18,
    padding: 20,
    marginBottom: 15,
  },

  label: {
    color: "#9CA3AF",
    fontSize: 16,
  },

  value: {
    color: "#00FF99",
    fontSize: 28,
    fontWeight: "bold",
    marginTop: 8,
  },
});
