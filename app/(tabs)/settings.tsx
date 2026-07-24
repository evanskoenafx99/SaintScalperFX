import { View, Text, StyleSheet } from "react-native";

export default function SettingsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Settings</Text>

      <View style={styles.card}>
        <Text style={styles.option}>🎨 Theme</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.option}>🤖 AI Avatar</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.option}>🔔 Notifications</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.option}>🔗 Connect MT5</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.option}>🌐 Connect AI Bridge</Text>
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

  option: {
    color: "#FFFFFF",
    fontSize: 18,
  },
});
